from django.urls import path

from watchlist.views import WatchlistTickerView, RemoveWatchlistView, WatchlistView

# v1/watchlist/
urlpatterns = [
    # v1/watchlist/
    path("", WatchlistView.as_view()),
    # v1/watchlist/<str:ticker_id>/add/
    path("<str:ticker_id>/add/", WatchlistTickerView.as_view()),
    # v1/watchlist/<str:watchlist_id>/remove/
    path("<str:watchlist_item_id>/remove/", RemoveWatchlistView.as_view()),
]
