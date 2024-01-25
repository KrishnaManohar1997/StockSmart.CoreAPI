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
from stocksmart.celery import app
from common.helper.datetime_helper import DateTimeHelper
from common.helper.market_status import (
    get_yesterday_market_times,
    is_market_open_on_day,
)

logger = structlog.getLogger("django.server")


import requests


class PostTickerPriceUpdater:

    PREV_MARKET_OPEN_TIME_UTC = None
    PREV_MARKET_CLOSE_TIME_UTC = None
    PREV_MARKET_OPEN_TIME_UTC_MS = None
    PREV_MARKET_CLOSE_TIME_UTC_MS = None

    @staticmethod
    def initialize_prev_day_market_times():
        # Previous Day Market Opening and Closing time
        (
            PostTickerPriceUpdater.PREV_MARKET_OPEN_TIME_UTC,
            PostTickerPriceUpdater.PREV_MARKET_CLOSE_TIME_UTC,
        ) = get_yesterday_market_times(as_utc=True)

        # Previous Day Market Opening and Closing time in Epoch MilliSeconds
        PostTickerPriceUpdater.PREV_MARKET_OPEN_TIME_UTC_MS = (
            DateTimeHelper.get_epoch_milliseconds_from_datetime(
                PostTickerPriceUpdater.PREV_MARKET_OPEN_TIME_UTC
            )
        )
        PostTickerPriceUpdater.PREV_MARKET_CLOSE_TIME_UTC_MS = (
            DateTimeHelper.get_epoch_milliseconds_from_datetime(
                PostTickerPriceUpdater.PREV_MARKET_CLOSE_TIME_UTC
            )
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
            target_price__isnull=False,
        )
        # Status of market, True if Opened, False if Closed
        market_status = is_market_open_on_day(prev_day_start)
        PostTickerPriceUpdater.map_ticker_market_price(posts, market_status)

    @staticmethod
    def get_stock_quotes_between(stock_symbol, start_time, end_time):
        url = f"https://groww.in/v1/api/charting_service/v2/chart/exchange/NSE/segment/CASH/{stock_symbol}"
        params = {
            "intervalInMinutes": 1,
            "startTimeInMillis": start_time,
            "endTimeInMillis": end_time,
        }
        return requests.get(url, params=params)

    @staticmethod
    def get_market_price_for_stock(
        stock_symbol, post_created_at, stocks_minute_data, ticker_prev_ltp_map
    ):
        CLOSING_INDEX_IN_CANDLE = 4
        # When Post is Created in B/w Market Open Hours
        # Use the Ticker Price Value, which is nearest full minute from Post Created Time
        if (
            post_created_at >= PostTickerPriceUpdater.PREV_MARKET_OPEN_TIME_UTC
            and post_created_at <= PostTickerPriceUpdater.PREV_MARKET_CLOSE_TIME_UTC
        ):
            timediff = (
                post_created_at - PostTickerPriceUpdater.PREV_MARKET_OPEN_TIME_UTC
            ).seconds
            if timediff <= 60:
                candle_index = 1
            else:
                candle_index = int(timediff / 60)
            # When Tickers have no trading Activity
            # Number of Candles will differ, So Using LTP
            if candle_index > len(stocks_minute_data):
                candle_index = -1
            return stocks_minute_data[candle_index][CLOSING_INDEX_IN_CANDLE]

        # If Post is Created after Market is Closed
        # Use the last close price
        if post_created_at > PostTickerPriceUpdater.PREV_MARKET_CLOSE_TIME_UTC:
            # 0TS 1-O 2-H 3-L 4-C
            return stocks_minute_data[-1][CLOSING_INDEX_IN_CANDLE]

        # If Post is created Before Market Open hours
        # Use Previous Days LTP
        return ticker_prev_ltp_map.get(stock_symbol)

    @staticmethod
    def bulk_update_post_ticker_mkt_price(posts):
        return Post.objects.bulk_update(posts, ["ticker_mkt_price_at_post"])

    @staticmethod
    def map_ticker_market_price(posts, is_market_open):
        stock_symbols = list(set(posts.values_list("source__symbol", flat=True)))

        if not is_market_open:
            ticker_ltp_map = dict(
                Stock.objects.filter(symbol__in=stock_symbols).values_list(
                    "symbol", "ltp"
                )
            )
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

        # Market Opened Scenario
        logger.info("Processing posts for Prev Market Opened Scenario ")
        ticker_prev_ltp_map = dict(
            Stock.objects.filter(symbol__in=stock_symbols).values_list(
                "symbol", "prev_ltp"
            )
        )
        for symbol in stock_symbols:
            updated_post_objs = []
            logger.info("Processing posts for Ticker ", symbol=symbol)
            response = PostTickerPriceUpdater.get_stock_quotes_between(
                symbol,
                PostTickerPriceUpdater.PREV_MARKET_OPEN_TIME_UTC_MS,
                PostTickerPriceUpdater.PREV_MARKET_CLOSE_TIME_UTC_MS,
            )
            response_data = response.json()
            stocks_minute_data = response_data["candles"]
            for post in posts.filter(source__symbol=symbol):
                post.ticker_mkt_price_at_post = (
                    PostTickerPriceUpdater.get_market_price_for_stock(
                        symbol, post.created_at, stocks_minute_data, ticker_prev_ltp_map
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
