from common.base_view import PublicBaseView
from news.serializers import NewsSerializer
from news.services import NewsService
from smallcase.services import SmallcaseService
from stock.services import StockService


class NewsView(PublicBaseView):
    stock_service = StockService()
    news_service = NewsService()
    smallcase_service = SmallcaseService()
    news_serializer = NewsSerializer

    TICKER_NEWS_LIMIT = 10

    def __invalid_request(self):
        return self.bad_request_response("Invalid request")

    def post(self, request):
        ticker_type = request.data.get("type", "stock").lower()
        symbol = request.data.get("symbol")
        if not symbol:
            return self.__invalid_request()
        if ticker_type == "stock":
            stock = self.stock_service.get_stock_by_symbol(symbol)
            if not stock:
                return self.__invalid_request()
            news_queryset = self.news_service.fetch_ticker_news(stock)[
                : self.TICKER_NEWS_LIMIT
            ]
        elif ticker_type == "smallcase":
            smallcase = self.smallcase_service.get_smallcase_by_symbol_or_none(symbol)
            if not smallcase:
                return self.__invalid_request()
            news_queryset = self.news_service.fetch_smallcase_news(smallcase)[
                : self.TICKER_NEWS_LIMIT
            ]
        else:
            return self.__invalid_request()
        news_data = self.news_serializer(news_queryset, many=True).data
        return self.data_response(message="News", data=news_data)
