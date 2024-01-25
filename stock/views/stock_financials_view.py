from stock.services import StockFinancialsService, StockService
from stock.serializers import StockFinancialsSerializer
from common.base_view import PublicBaseView


class StockFinancialsView(PublicBaseView):
    serializer = StockFinancialsSerializer
    stock_service = StockService()
    stock_financials_service = StockFinancialsService()

    def get(self, request, symbol: str):

        stock = self.stock_service.get_stock_by_symbol(symbol)
        if not stock:
            return self.resource_not_found_response("Stock", symbol)
        statement = self.stock_financials_service.financials_filter(stock, request)

        data = self.serializer(statement, many=True).data
        return self.data_response("Ok", data)
