from watchlist.models import Watchlist, WatchlistItem


class WatchlistRepository:
    def get_watchlist_items(self, user):
        return (
            WatchlistItem.objects.filter(created_by_user=user)
            .order_by("-created_at")
            .prefetch_related("content_object")
            .select_related("content_type")
        )

    def get_watchlist_count(self, user):
        return user.watchlist.watchlist_items.count()

    def add_watchlist_item(self, user, item):
        return WatchlistItem.objects.create(
            watchlist=user.watchlist, created_by_user_id=user.id, content_object=item
        )

    def remove_watchlist_item(self, watchlist):
        watchlist.delete()

    def watchlist_item_by_id(self, watchlist, watchlist_item_id):
        return WatchlistItem.objects.get(watchlist=watchlist, id=watchlist_item_id)
