from watchlist.serializers import WatchlistItemSerializer
from common.base_view import BaseView
from watchlist.services import WatchlistService


class WatchlistView(BaseView):
    watchlist_service = WatchlistService()

    def get(self, request):
        user_watchlist_queryset = self.watchlist_service.get_watchlist_items(
            request.user
        )
        watchlist_data = WatchlistItemSerializer(
            user_watchlist_queryset, many=True
        ).data
        return self.data_response("Watchlist", watchlist_data)
