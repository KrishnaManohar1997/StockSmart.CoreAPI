from django.core.cache import cache

from common.base_view import PublicBaseView
from mentions.serializers.post_stock_mention_serializer import (
    PostStockMentionSerializer,
)
from mentions.services.ticker_mention_service import TickerMentionService
from stock.serializers import SearchStockSerializer
from stock.services import StockService


class TrendingStocksView(PublicBaseView):
    serializer = PostStockMentionSerializer
    stock_service = StockService()
    ticker_mention_service = TickerMentionService()
    CACHE_KEY = "TRENDING_STOCKS"
    CACHE_TTL = 60 * 15

    def get(self, request):
        # Retrieves the Trending Stocks Ids
        trending_stocks = cache.get(self.CACHE_KEY)
        if not trending_stocks:
            trending_stock_ids = list(
                dict(self.ticker_mention_service.get_trending_stocks()).keys()
            )
            # Fetches all the Tickers
            trending_stocks = SearchStockSerializer(
                self.stock_service.get_stocks_by_ids(trending_stock_ids), many=True
            ).data

            cache.set(
                self.CACHE_KEY,
                trending_stocks,
                timeout=self.CACHE_TTL,
            )

        # Gets Latest Posts for the Mentioned Tickers
        for stock in trending_stocks:
            stock["posts"] = self.serializer(
                self.ticker_mention_service.get_ticker_mentioned_latest_posts(
                    stock["id"]
                )[:2],
                many=True,
            ).data

        return self.data_response(message="", data=trending_stocks)
