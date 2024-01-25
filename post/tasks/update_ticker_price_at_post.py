# This worker helps in updating the Market Price of Ticker @ Post time
# This Job is executed Everday @ 1AM
# This job only considers Posts of the previous day

# ! RULES
# If Market is opened in the previous day
# Any Post before Market Hours will use the LTP on Ticker
# Any Post created in the Market Open Hours will use the nearest Minute's Market Price
# Any Post Created after market close will use the LTP (last Minute) of that day

import structlog
from post.models import Post
from stock.models import Stock
from stock_data_source.ticker_data_helper import TickerDataHelper
from stocksmart.celery import app
from common.helper.datetime_helper import DateTimeHelper
from common.helper.market_status import (
    get_yesterday_market_times,
    is_market_open_on_day,
)

logger = structlog.getLogger("django.server")


class PostTickerPriceUpdater:

    PREV_MARKET_OPEN_TIME_UTC = None
    PREV_MARKET_CLOSE_TIME_UTC = None

    PREV_MARKET_OPEN_TIME = None
    PREV_MARKET_CLOSE_TIME = None

    @staticmethod
    def initialize_prev_day_market_times():
        # Previous Day Market Opening and Closing time UTC
        (
            PostTickerPriceUpdater.PREV_MARKET_OPEN_TIME_UTC,
            PostTickerPriceUpdater.PREV_MARKET_CLOSE_TIME_UTC,
        ) = get_yesterday_market_times(as_utc=True)

        # Previous Day Market Opening and Closing time
        market_open_time, market_close_time = get_yesterday_market_times()
        PostTickerPriceUpdater.PREV_MARKET_OPEN_TIME = market_open_time.replace(
            tzinfo=None
        )
        PostTickerPriceUpdater.PREV_MARKET_CLOSE_TIME = market_close_time.replace(
            tzinfo=None
        )

    @staticmethod
    def start():
        PostTickerPriceUpdater.initialize_prev_day_market_times()
        prev_day_start, prev_day_end = DateTimeHelper.get_prev_day_start_and_end()
        prev_day_start_utc = DateTimeHelper.get_utc_timezone_date(prev_day_start)
        prev_day_end_utc = DateTimeHelper.get_utc_timezone_date(prev_day_end)

        posts = Post.objects.filter(
            created_at__gte=prev_day_start_utc,
            created_at__lte=prev_day_end_utc,
            source__ticker_type="Stock",
        )
        # Status of market, True if Opened, False if Closed
        market_status = is_market_open_on_day(prev_day_start_utc)
        PostTickerPriceUpdater.map_ticker_market_price(posts, market_status)

    @staticmethod
    def get_market_price_for_stock(
        stock_symbol, post_created_at, stocks_minute_data, ticker_ltp_map
    ):
        # When Post is Created in B/w Market Open Hours
        # Use the Ticker Price Value, which is nearest full minute from Post Created Time
        if (
            post_created_at <= PostTickerPriceUpdater.PREV_MARKET_OPEN_TIME_UTC
            and post_created_at >= PostTickerPriceUpdater.PREV_MARKET_CLOSE_TIME_UTC
        ):
            timediff = (
                post_created_at - PostTickerPriceUpdater.PREV_MARKET_OPEN_TIME_UTC
            )
            candle_index = int((timediff).seconds / 60)
            return stocks_minute_data[candle_index][4]

        # If Post is Created after Market is Closed
        # Use the last close price
        if post_created_at > PostTickerPriceUpdater.PREV_MARKET_CLOSE_TIME_UTC:
            # 0TS 1-O 2-H 3-L 4-C
            return stocks_minute_data[-1][4]

        # If Post is created Before Market Open hours
        # Use Previous Days LTP
        return ticker_ltp_map.get(stock_symbol)

    @staticmethod
    def bulk_update_post_ticker_mkt_price(posts):
        return Post.objects.bulk_update(posts, ["ticker_mkt_price_at_post"])

    @staticmethod
    def map_ticker_market_price(posts, is_market_open):

        stock_symbols = list(set(posts.values_list("source__symbol", flat=True)))

        ticker_ltp_map = dict(
            Stock.objects.filter(symbol__in=stock_symbols).values_list(
                "symbol", "industry"
            )
        )

        if not is_market_open:
            logger.info("Processing Posts for a Market Closed Day")
            updated_post_objs = []
            for post in posts:
                post.ticker_mkt_price_at_post = ticker_ltp_map.get(
                    post.source.get("symbol")
                )
                updated_post_objs.append(post)
            PostTickerPriceUpdater.bulk_update_post_ticker_mkt_price(updated_post_objs)
            logger.info("Updated LTP's on Posts")
            return

        logger.info("Processing posts for Prev Market Opened Scenario ")
        updated_post_objs = []
        for symbol in stock_symbols:
            logger.info("Processing posts for Ticker ", symbol=symbol)
            response_data = TickerDataHelper().get_ticker_data_by_minute_interval(
                symbol,
                PostTickerPriceUpdater.PREV_MARKET_OPEN_TIME,
                PostTickerPriceUpdater.PREV_MARKET_CLOSE_TIME,
            )
            if not response_data.get("is_valid"):
                logger.error(
                    f"Couldn't retrieve Minute Candle data for {symbol} - {response_data.get('message')}"
                )
            stocks_minute_data = response_data.get("data")
            for post in posts.filter(source__symbol=symbol):
                post.ticker_mkt_price_at_post = (
                    PostTickerPriceUpdater.get_market_price_for_stock(
                        symbol, post.created_at, stocks_minute_data, ticker_ltp_map
                    )
                )
                updated_post_objs.append(post)
        PostTickerPriceUpdater.bulk_update_post_ticker_mkt_price(updated_post_objs)
        logger.info("Updated LTP's on Posts")


@app.task()
def update_ticker_price_at_post():
    logger.info("Ticker Price Mapping for Posts Job Started")
    try:
        PostTickerPriceUpdater.start()
        logger.info("Ticker Price Mapping for Posts Job Ended")
    except Exception as error:
        logger.error(f"Ticker Price Mapping for Posts Job Failed --> {error}")
