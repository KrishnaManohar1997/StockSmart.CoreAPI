from django.urls import path

from stock.views import (
    StockSearchView,
    TrendingStocksView,
    StockListView,
    StockDetailsView,
    TickerStocksView,
    StockFinancialsView,
    StockOverviewView,
)

# v1/stocks/
urlpatterns = [
    # v1/stocks/
    path("", StockListView.as_view()),
    # v1/stocks/tape/
    path("ticker-stocks/", TickerStocksView.as_view()),
    # v1/stocks/search/
    path("search/", StockSearchView.as_view()),
    # v1/stocks/trending-stocks/
    path("trending-stocks/", TrendingStocksView.as_view()),
    # v1/stocks/<symbol>/
    path("<str:symbol>/", StockDetailsView.as_view()),
    # v1/stocks/<symbol>/overview
    path("<str:symbol>/overview", StockOverviewView.as_view()),
    # v1/stocks/<symbol>/financials
    path("<str:symbol>/financials", StockFinancialsView.as_view()),
]
