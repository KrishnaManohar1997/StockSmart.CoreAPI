from stock.services import StockService
from stock.serializers import SearchStockSerializer
from common.base_view import PublicBaseView
from rest_framework.pagination import LimitOffsetPagination


class StockSearchView(PublicBaseView):

    serializer = SearchStockSerializer
    stock_service = StockService()
    paginator = LimitOffsetPagination()

    def get(self, request):
        stock_query = request.query_params.get("q")
        if not stock_query:
            return self.bad_request_response("No search")
        stocks_queryset = self.stock_service.get_stocks_by_name(stock_query)
        page = self.paginator.paginate_queryset(stocks_queryset, request)
        data = self.serializer(page, many=True).data
        return self.paginated_response(self.paginator, "Stocks found", data)
