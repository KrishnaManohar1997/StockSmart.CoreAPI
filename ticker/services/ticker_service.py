from ticker.repositories.ticker_repository import TickerRepository
from smallcase.services.smallcase_service import SmallcaseService
from stock.services.stock_service import StockService
from django.core.exceptions import ValidationError


class TickerService(SmallcaseService, StockService):
    ticker_repo = TickerRepository()

    def get_ticker_by_id(self, ticker_id, ticker_type):
        if not ticker_id:
            raise ValidationError("Invalid Request")
        ticker = None
        if ticker_type == "Stock":
            ticker = self.get_stock_by_id(ticker_id)
        if ticker_type == "Smallcase":
            ticker = self.get_smallcase_by_id_or_none(ticker_id)
        if not ticker:
            raise ValidationError("Unknown ticker")
        return ticker

    def get_ticker_by_symbol(self, ticker_symbol, ticker_type):
        if not ticker_symbol:
            raise ValidationError("Invalid Request")
        ticker = None
        if ticker_type == "Stock":
            ticker = self.get_stock_by_symbol(ticker_symbol)
        if ticker_type == "Smallcase":
            ticker = self.get_smallcase_by_symbol_or_none(ticker_symbol)
        if not ticker:
            raise ValidationError("Unknown ticker")
        return ticker

    def get_ticker_mentioned_posts(self, ticker, exclude_created_by_users):
        return self.ticker_repo.get_ticker_mentioned_posts(
            ticker, exclude_created_by_users
        )
