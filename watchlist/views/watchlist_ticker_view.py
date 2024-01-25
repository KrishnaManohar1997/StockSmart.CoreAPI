from watchlist.serializers import AddWatchlistItemSerializer
from django.core.exceptions import ValidationError
from smallcase.services.smallcase_service import SmallcaseService
from stock.services.stock_service import StockService
from common.base_view import BaseView
from watchlist.services import WatchlistService


class WatchlistTickerView(BaseView):
    watchlist_service = WatchlistService()
    stock_service = StockService()
    smallcase_service = SmallcaseService()
    serializer = AddWatchlistItemSerializer

    def get_ticker_by_id(self, ticker_id, ticker_type):
        ticker = None
        if ticker_type == "Stock":
            ticker = self.stock_service.get_stock_by_id(ticker_id)
        if ticker_type == "Smallcase":
            ticker = self.smallcase_service.get_smallcase_by_id_or_none(ticker_id)
        if not ticker:
            raise ValidationError("Unknown ticker")
        return ticker

    def post(self, request, ticker_id: str):
        ticker = self.get_ticker_by_id(
            ticker_id, request.data.get("ticker_type", "Stock")
        )
        data = {
            "created_by_user": request.user.id,
            "object_id": ticker.id,
            "watchlist": request.user.watchlist.id,
        }
        watchlist_item_serializer = self.serializer(data=data)
        if watchlist_item_serializer.is_valid():
            is_created, watchlist_item = self.watchlist_service.add_watchlist_item(
                request.user, ticker
            )
            if not is_created:
                return self.bad_request_response("You have reached the Exhaust limit")
            return self.resource_created_response("Watchlist", watchlist_item.id)
        return self.serializer_error_response(
            message="Watchlist Item cannot be added",
            serializer_errors=watchlist_item_serializer.errors,
        )
