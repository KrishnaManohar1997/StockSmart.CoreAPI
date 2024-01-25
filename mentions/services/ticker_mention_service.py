from mentions.repositories import PostTickerMentionRepository
from django.conf import settings

MAX_TRENDING_STOCKS = settings.MAX_TRENDING_STOCKS


class TickerMentionService:
    post_ticker_mention_repo = PostTickerMentionRepository()

    def create_post_ticker_mentions(self, post, tickers: list):
        post_id = post.id
        created_by_user_id = post.created_by_user_id
        return self.post_ticker_mention_repo.create_post_ticker_mentions(
            post_id, created_by_user_id, tickers
        )

    def get_trending_stocks(self):
        return self.post_ticker_mention_repo.get_trending_stocks()[:MAX_TRENDING_STOCKS]

    def get_ticker_mentioned_latest_posts(self, ticker_id):
        return self.post_ticker_mention_repo.get_ticker_mentioned_latest_posts(
            ticker_id
        )
