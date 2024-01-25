from django.core.cache import cache

from common.base_view import PublicBaseView
from common.helper.market_status import get_next_market_open_time
from stock.services import StockService


class TickerStocksView(PublicBaseView):
    stock_service = StockService()
    CACHE_KEY = "TICKER_TAPE"

    def get(self, request):
        data = cache.get(self.CACHE_KEY)
        if data:
            return self.data_response("", data)
        data = self.stock_service.get_stock_quotes()
        cache.set(self.CACHE_KEY, data, timeout=get_next_market_open_time())
        return self.data_response("", data)
