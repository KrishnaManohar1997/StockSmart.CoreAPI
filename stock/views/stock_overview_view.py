from stock.services import StockService
from stock.serializers import StockOverviewSerializer
from common.base_view import PublicBaseView


class StockOverviewView(PublicBaseView):
    serializer = StockOverviewSerializer
    stock_service = StockService()

    def get(self, request, symbol: str):
        stock = self.stock_service.get_stock_by_symbol(symbol)
        if not stock:
            return self.resource_not_found_response("Stock", symbol)
        data = self.serializer(stock).data
        return self.data_response("Ok", data)
