from django.db.models.query import QuerySet
from stock.repositories import StockRepository


class StockService:
    stock_repository = StockRepository()

    def get_stocks_matching_by_symbol_or_name(self, stock_name: str) -> QuerySet:
        """
        Returns top matching records based on the Stock Name
        Only 10 records will be returned, when more than 10 records exist

        Args:
            stock_name (str): Name of the stock or Symbol of the Stock

        Returns:
            QuerySet: QuerySet of matching Stock Records
        """
        return self.stock_repository.get_stocks_matching_by_symbol_or_name(stock_name)
