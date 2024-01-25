from common.base_view import BaseView
from watchlist.services import WatchlistService


class RemoveWatchlistView(BaseView):
    watchlist_service = WatchlistService()

    def post(self, request, watchlist_item_id: str):
        watchlist_item = self.watchlist_service.watchlist_item_by_id_or_none(
            request.user.watchlist, watchlist_item_id
        )
        if not watchlist_item:
            return self.resource_not_found_response("Watchlist", watchlist_item_id)
        self.watchlist_service.remove_watchlist_item(watchlist_item)
        return self.resource_deleted_response(
            "Watchlist item removed", watchlist_item_id
        )
