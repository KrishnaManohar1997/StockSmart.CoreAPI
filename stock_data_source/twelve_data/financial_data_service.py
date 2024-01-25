import requests

from . import BaseDataService


class FinancialDataService(BaseDataService):
    def __get_params(self, ticker_symbol, exchange):
        params = {
            "apikey": self.API_KEY,
            "symbol": ticker_symbol,
            "exchange": exchange,
        }
        
        return params
    def get_ticker_income_statement(
        self, ticker_symbol: str, period: str = "annual", exchange: str = "NSE"
    ):
        ticker_symbol = ticker_symbol.replace("-", ".")
        url = f"{self.BASE_URL}/income_statement"
        params = self.__get_params(ticker_symbol, exchange)

        return requests.get(url, params=params)

    def get_ticker_cash_flow(self, ticker_symbol: str, exchange: str = "NSE"):
        ticker_symbol = ticker_symbol.replace("-", ".")
        url = f"{self.BASE_URL}/cash_flow"
        params = self.__get_params(ticker_symbol, exchange)

        return requests.get(url, params=params)

    def get_ticker_balance_sheet(self, ticker_symbol: str, exchange: str = "NSE"):
        ticker_symbol = ticker_symbol.replace("-", ".")
        url = f"{self.BASE_URL}/balance_sheet"
        params = self.__get_params(ticker_symbol, exchange)
        return requests.get(url, params=params)

