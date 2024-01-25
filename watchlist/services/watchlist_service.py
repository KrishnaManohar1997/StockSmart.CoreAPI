from watchlist.models import WatchlistItem
from watchlist.repositories import WatchlistRepository


class WatchlistService:
    watchlist_repo = WatchlistRepository()

    # When Multiple Watchlists Concept is applied
    # Make sure to pass the Watchlist Id
    def get_watchlist_items(self, user):
        return self.watchlist_repo.get_watchlist_items(user)

    def is_watchlist_add_valid(self, user) -> bool:
        watchlist_count = self.get_watchlist_count(user)
        user_watchlist_limit = 10
        # Broker Logged in user
        if user.is_broker_connected():
            user_watchlist_limit += 10
        return watchlist_count < user_watchlist_limit

    def get_watchlist_count(self, user):
        return self.watchlist_repo.get_watchlist_count(user)

    def add_watchlist_item(self, user, item):
        if not self.is_watchlist_add_valid(user):
            return False, None
        return True, self.watchlist_repo.add_watchlist_item(user, item)

    def remove_watchlist_item(self, watchlist):
        self.watchlist_repo.remove_watchlist_item(watchlist)

    def watchlist_item_by_id_or_none(self, watchlist, watchlist_item_id):
        try:
            return self.watchlist_repo.watchlist_item_by_id(
                watchlist, watchlist_item_id
            )
        except WatchlistItem.DoesNotExist:
            return None
