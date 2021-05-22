from stock.services.stock_service import StockService
from stock.serializers import StockSerializer
from common.base_view import BaseView


class StockView(BaseView):
    stock_service = StockService()

    # Filters the Stocks based on the Stock name or Symbol
    def get(self, request):
        stock_name = request.query_params.get("stock", None)
        if not stock_name:
            return self.bad_request_response("Expected parameter stock is missing")
        stocks_list = self.stock_service.get_stocks_matching_by_symbol_or_name(
            stock_name
        )
        stock_data = StockSerializer(stocks_list, many=True).data
        return self.data_response(message="Found the following stocks", data=stock_data)
