from .ticker_mention_service import TickerMentionService
from .user_mention_service import UserMentionService


class MentionService:
    def create_post_mentions(self, post, tickers: list, users: list):
        return (
            UserMentionService().create_post_user_mentions(post, users),
            TickerMentionService().create_post_ticker_mentions(post, tickers),
        )
