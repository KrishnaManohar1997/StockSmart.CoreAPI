import requests
import structlog

from stock.models import Stock
from stock.repositories import StockRepository

logger = structlog.getLogger("django.server")

SID_STOCK_MAPPER = {
    "RELI": "RELIANCE",
    "TCS": "TCS",
    "INFY": "INFY",
    "HLL": "HINDUNILVR",
    "SBI": "SBIN",
    "HDBK": "HDFCBANK",
    "MAHM": "M&M",
    "CYIE": "CYIENT",
    "NIIT": "NIITLTD",
    "DIVI": "DIVISLAB",
    "NBES": "NIFTYBEES",
    "FNXC": "FINCABLES",
    "SUN": "SUNPHARMA",
    "TACN": "TATACONSUM",
    "TISC": "TATASTEEL",
    "ITC": "ITC",
    "JUBI": "JUBLFOOD",
    "INGL": "INDIGO",
    "HPCL": "HINDPETRO",
    "BRTI": "BHARTIARTL",
    "TTCH": "TATACHEM",
}
sids = ",".join(SID_STOCK_MAPPER.keys())

nse_tape_stocks = [s + ":NSE" for s in SID_STOCK_MAPPER.values()]

INDEX_AND_TAPE_STOCKS = ["NSEI", "BSESN"] + nse_tape_stocks


class StockService:
    stock_repo = StockRepository()

    def get_stocks_by_name(self, stock_name: str):
        return self.stock_repo.get_stocks_by_name_or_symbol_search(stock_name)

    def get_stock_by_symbol(self, stock_symbol: str):
        try:
            return self.stock_repo.get_stock_by_symbol(stock_symbol.upper())
        except Stock.DoesNotExist:
            return None

    def get_stock_by_id(self, stock_id: str):
        try:
            return self.stock_repo.get_stock_by_id(stock_id)
        except Stock.DoesNotExist:
            return None

    def get_stock_mention_posts(self, stock, blocked_by_user_ids: list):
        return self.stock_repo.get_stock_mention_posts(stock, blocked_by_user_ids)

    def get_stocks_by_symbols(self, stock_symbols: list):
        return self.stock_repo.get_stocks_by_symbols(stock_symbols)

    def get_stocks_by_ids(self, stock_ids: list):
        return self.stock_repo.get_stocks_by_ids(stock_ids)

    def get_all_stocks(self):
        return self.stock_repo.get_all_stocks()

    def __stocksmart_tt_mapper(self, data: dict):
        return {
            "symbol": SID_STOCK_MAPPER[data["sid"]],
            "open": data["o"],
            "close": data["c"],
            "high": data["h"],
            "low": data["l"],
            "price": data["price"],
            "change": data["change"],
        }

    def get_allowed_trending_stocks_list_ids(self):
        # TODO: Remove when Websockets are Added
        return self.stock_repo.get_stocks_by_symbols(list(SID_STOCK_MAPPER.values()))

    def get_stock_quotes(self):
        try:
            url = f"https://quotes-api.tickertape.in/quotes?sids={sids}"
            response = requests.get(url)
            if response.status_code == 200:
                return [
                    self.__stocksmart_tt_mapper(_) for _ in response.json().get("data")
                ]
        except Exception as e:
            logger.info(f"Error getting prices of Stocks for Ticker Bar {e}")
        return {}
