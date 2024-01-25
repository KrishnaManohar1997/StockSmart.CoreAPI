# This worker helps in updating the Market Price of Ticker @ Post time
# This Job is executed Everday @ 1AM
# This job only considers Posts of the previous day

# ! RULES
# If Market is opened in the previous day
# Any Post before Market Hours will use the LTP on Ticker
# Any Post created in the Market Open Hours will use the nearest Minute's Market Price
# Any Post Created after market close will use the LTP (last Minute) of that day

import json

import requests
import structlog

from common.helper.datetime_helper import DateTimeHelper
from common.helper.market_status import is_market_open_on_day
from stock.models import Stock
from stocksmart.celery import app

logger = structlog.getLogger("django.server")


def ticker_data_helper():
    """
    {
        "isin": "INE002A01018",
        "growwContractId": "GSTK500325",
        "companyName": "Reliance Industries",
        "companyShortName": "Reliance Industries",
        "searchId": "reliance-industries-ltd",
        "industryCode": null,
        "bseScriptCode": 500325,
        "nseScriptCode": "RELIANCE",
        "yearlyHighPrice": 2750.0,
        "yearlyLowPrice": 1830.0,
        "closePrice": 2455.85,
        "marketCap": 1660680362120760,
        "livePriceDto": {
            "type": "LIVE_PRICE",
            "symbol": "RELIANCE",
            "tsInMillis": 1639386301,
            "open": 2473.5,
            "high": 2474.1,
            "low": 2404.0,
            "close": 2458.95,
            "ltp": 2419.0,
            "dayChange": -39.94999999999982,
            "dayChangePerc": -1.6246771996177158,
            "lowPriceRange": 2213.1,
            "highPriceRange": 2704.8,
            "volume": 4423924,
            "totalBuyQty": 306475.0,
            "totalSellQty": 1776974.0,
            "lastTradeQty": 1,
            "lastTradeTime": 1639366501
        }
    }
    """
    url = "https://groww.in/v1/api/stocks_data/v1/all_stocks"

    payload = json.dumps(
        {
            "listFilters": {"INDUSTRY": [], "INDEX": []},
            "objFilters": {
                "MARKET_CAP": {
                    "min": 0,
                    "max": 2000000000000000,
                    "enabled": False,
                    "ranges": {
                        "Small": [0, 500000],
                        "Large": [0, 2000000],
                        "Mid": [0, 20000000],
                    },
                },
                "CLOSE_PRICE": {
                    "min": 0,
                    "max": 100000,
                    "enabled": False,
                    "ranges": {},
                },
            },
            "sortBy": "NA",
            "sortType": "ASC",
            "size": 5000,
            "page": 0,
        }
    )
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, headers=headers, data=payload, timeout=10)
    if response.status_code != 200:
        return {
            "is_valid": False,
            "message": f"API response : {response.status_code} -  {response.json()}",
        }
    return {"is_valid": True, "data": response.json().get("records")}


class TickerPriceUpdater:
    @staticmethod
    def start():
        today_start = DateTimeHelper.get_today_start_and_end()[0]
        is_market_open = is_market_open_on_day(today_start)
        today = today_start.replace(tzinfo=None)
        if not is_market_open:
            logger.info(
                f"Market is closed on day : {today} INDIA, Job terminated to update Ticker Prices"
            )
            return
        TickerPriceUpdater.update_ticker_data()

    @staticmethod
    def map_ticker_data(ticker_objs_dict, tickers_data, update_keys):
        key_map = {"ltp": "ltp", "prev_ltp": "close", "high": "high", "low": "low"}
        updated_ticker_objs = []
        for ticker_item in tickers_data:
            ticker_symbol = ticker_item.get("nseScriptCode")
            if not ticker_symbol:
                continue
            ticker_obj = ticker_objs_dict.pop(ticker_symbol, None)
            if not ticker_obj:
                logger.info(f"Missing Ticker in DB : {ticker_symbol}")
                continue
            price_dto = ticker_item.get("livePriceDto")
            # High, Low, Prev Close and LTP Close-Today
            for key in update_keys:
                setattr(ticker_obj, key, price_dto.get(key_map.get(key)))
            updated_ticker_objs.append(ticker_obj)
        return updated_ticker_objs

    @staticmethod
    def update_ticker_data():
        response_obj = ticker_data_helper()
        if not response_obj.get("is_valid"):
            logger.error(
                f"Error retreiving Tickers Data - {response_obj.get('message')}"
            )
            return
        response_data = response_obj.get("data")
        if not response_data:
            logger.error(f"Empty data for Ticker Symbols")
            return

        ticker_objs_dict = {
            ticker.symbol: ticker for ticker in list(Stock.objects.all())
        }
        UPDATE_KEYS = ["ltp", "prev_ltp", "high", "low"]
        updated_ticker_objects = TickerPriceUpdater.map_ticker_data(
            ticker_objs_dict, response_data, UPDATE_KEYS
        )

        Stock.objects.bulk_update(updated_ticker_objects, UPDATE_KEYS)
        logger.info("Updated Tickers with LTP's")


@app.task(autoretry_for=(Exception,), retry_kwargs={"max_retries": 3, "countdown": 15})
def update_ticker_prices():
    logger.info("Update Ticker Quotes Job Started")
    try:
        TickerPriceUpdater.start()
        logger.info("Update Ticker Quotes Job Executed Successfully")
    except Exception as error:
        logger.error(f"Update Ticker Quotes Job  Failed --> {error}")
        raise Exception("Retry Ticker Quotes Updation")
