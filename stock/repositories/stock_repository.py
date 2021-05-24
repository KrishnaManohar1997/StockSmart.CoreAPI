from django.db.models import Q
from django.db.models.query import QuerySet

from stock.models import Stock


class StockRepository:
    def get_stocks_matching_by_symbol_or_name(self, stock_name: str) -> QuerySet:
        """
        Returns top matching records based on the Stock Name
        Only 10 records will be returned, when more than 10 records exist

        Args:
            stock_name (str): Name of the stock or Symbol of the Stock

        Returns:
            QuerySet: QuerySet of matching Stock Records
        """

        # Maintaining the data in UpperCase for Consistency and
        # Optimized DB queries
        stock_name = stock_name.upper()
        stocks = Stock.objects.filter(is_deleted=False).filter(
            Q(name__contains=stock_name) | Q(symbol__contains=stock_name)
        )
        # Returns top 10 matching stocks
        return stocks if not stocks else stocks[:10]
