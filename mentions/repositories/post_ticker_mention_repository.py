from django.contrib.contenttypes.models import ContentType
from django.db.models import Count

from mentions.models import PostTickerMention


class PostTickerMentionRepository:
    def create_post_ticker_mentions(self, post_id, created_by_user_id, tickers: list):
        return PostTickerMention.objects.bulk_create(
            [
                PostTickerMention(
                    post_id=post_id,
                    ticker=ticker,
                    created_by_user_id=created_by_user_id,
                )
                for ticker in tickers
            ]
        )

    def get_trending_stocks(self):
        # TODO : Uncomment Following Line When Overall Trending Stocks is needed
        # And remove Filter by Id's of Specified Stocks
        from stock.services import StockService

        stock_ids = StockService().get_allowed_trending_stocks_list_ids()
        return (
            PostTickerMention.objects.filter(
                ticker_type=ContentType.objects.get(model="stock"),
                ticker_id__in=stock_ids,
            )
            .values_list("ticker_id")
            .annotate(ticker_count=Count("ticker_id"))
            .order_by("-ticker_count")
        )

    def get_ticker_mentioned_latest_posts(self, ticker_id):
        return (
            PostTickerMention.objects.filter(ticker_id=ticker_id)
            .select_related("post", "post__created_by_user")
            .order_by("-created_at")
        )
