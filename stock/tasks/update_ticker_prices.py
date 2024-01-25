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
    is_market_open_on_day,
)
from django.core.paginator import Paginator

logger = structlog.getLogger("django.server")


class TickerPriceUpdater:
    @staticmethod
    def start():
        prev_day_start = DateTimeHelper.get_prev_day_start_and_end()[0]
        is_market_open = is_market_open_on_day(prev_day_start)
        prev_day = prev_day_start.replace(tzinfo=None)
        if not is_market_open:
            logger.info(
                f"Market is closed on day : {prev_day} INDIA, Job terminated to update Ticker Prices"
            )
        TickerPriceUpdater.update_ticker_data()

    @staticmethod
    def map_ticker_data(ticker_objs, tickers_data):
        if len(tickers_data) != len(ticker_objs):
            logger.error("Mapping Error, Got two Lists of different length")
        for ticker, ticker_data in zip(ticker_objs, tickers_data):
            if ticker.symbol == ticker_data.get("symbol").replace(".", "-"):
                ticker.ltp = ticker_data.get("close")
                ticker.prev_ltp = ticker_data.get("previous_close")
            else:
                logger.error("Job Failed Ticker Symbol Not Found")

    @staticmethod
    def update_ticker_data():
        BATCH_SIZE = 5
        object_list = Stock.objects.exclude(symbol__icontains=".").order_by("symbol")
        stocks_paginator = Paginator(object_list, BATCH_SIZE)
        for page in stocks_paginator.page_range:
            ticker_objs = list(iter(stocks_paginator.get_page(page)))
            ticker_symbols = [s.symbol.replace("-", ".") for s in ticker_objs]
            response_obj = TickerDataHelper().get_quote_for_tickers_for_day(
                ticker_symbols
            )
            if not response_obj.get("is_valid"):
                logger.error(
                    f"Error retreiving Tickers Response for Page {page} - {response_obj.get('message')}"
                )
                return
            response_data = response_obj.get("data")
            if not response_data:
                logger.error(f"Empty data for Ticker Symbols on Page {page}")
                return
            TickerPriceUpdater.map_ticker_data(ticker_objs, response_data)
            return


@app.task(autoretry_for=(Exception,), retry_kwargs={"max_retries": 3, "countdown": 5})
def update_ticker_prices():
    logger.info("Update Ticker Quotes Job Started")
    try:
        TickerPriceUpdater.start()
        logger.info("Update Ticker Quotes Job Executed Successfully")
    except Exception as error:
        logger.error(f"Update Ticker Quotes Job  Failed --> {error}")
        raise Exception("Retrying the Job to Update Ticker Prices")
