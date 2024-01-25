from django.core.cache import cache

from stock.services import StockService
from stock.serializers import SearchStockSerializer
from common.base_view import PublicBaseView
from rest_framework.pagination import LimitOffsetPagination


class StockListView(PublicBaseView):

    serializer = SearchStockSerializer
    stock_service = StockService()
    paginator = LimitOffsetPagination()
    CACHE_KEY = "STOCKS_LIST"
    CACHE_TTL = 60 * 60 * 3

    def get(self, request):
        stocks_data = cache.get(self.CACHE_KEY)
        if stocks_data:
            return self.data_response("All stocks", stocks_data)
        stocks_queryset = self.stock_service.get_all_stocks()
        data = self.serializer(stocks_queryset, many=True).data
        cache.set(self.CACHE_KEY, data, timeout=self.CACHE_TTL)
        return self.data_response("All stocks", data)
