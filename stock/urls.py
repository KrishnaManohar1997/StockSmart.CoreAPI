from django.urls import path

from stock.views import StockView

urlpatterns = [
    # Stock View by stock filter
    path("", StockView.as_view()),
]
