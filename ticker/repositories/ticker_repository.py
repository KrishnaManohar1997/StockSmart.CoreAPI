class TickerRepository:
    def get_ticker_mentioned_posts(self, ticker, exclude_created_by_users):
        return ticker.post_set.exclude(
            created_by_user_id__in=exclude_created_by_users
        ).order_by("-created_at")
