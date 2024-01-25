import json

import requests

from . import BaseDataService


class TickerDataService(BaseDataService):
    REQUESTS_PER_MIN_LIMIT = 500

    def get_ticker_profile(self, ticker_symbol: str, exchange: str = "NSE"):
        ticker_symbol = ticker_symbol.replace("-", ".")
        url = f"{self.BASE_URL}/profile"
        params = {
            "symbol": ticker_symbol,
            "apikey": self.API_KEY,
            "exchange": exchange,
        }
        return requests.get(url, params=params)

    def get_ticker_statistics(self, ticker_symbol: str, exchange: str = "NSE"):
        ticker_symbol = ticker_symbol.replace("-", ".")
        url = f"{self.BASE_URL}/statistics"
        params = {
            "symbol": ticker_symbol,
            "apikey": self.API_KEY,
            "exchange": exchange,
        }
        return requests.get(url, params=params)

    def get_ticker_data_by_minute_interval(
        self, ticker_symbol: str, start_date, end_date, exchange: str = "NSE"
    ):
        url = f"{self.BASE_URL}/time_series"
        params = {
            "symbol": ticker_symbol,
            "interval": "1min",
            "apikey": self.API_KEY,
            "exchange": exchange,
            "timezone": "Asia/Calcutta",
            "start_date": str(start_date),
            "end_date": str(end_date),
            "dp": self.DECIMAL_POINTS,
            "order": "ASC",
        }
        return requests.get(url, params=params)

    def get_quote_for_tickers_for_day(
        self, ticker_symbols: list, exchange: str = "NSE"
    ):
        url = f"{self.BASE_URL}/complex_data"
        params = {"apikey": self.API_KEY}
        headers = {"Content-Type": "application/json"}
        payload = json.dumps(
            {
                "symbols": ticker_symbols,
                "intervals": ["1day"],
                "exchange": exchange,
                "order": "ASC",
                "timezone": "Asia/Calcutta",
                "dp": 2,
                "methods": ["quote"],
            }
        )
        return requests.post(url, headers=headers, data=payload, params=params)
