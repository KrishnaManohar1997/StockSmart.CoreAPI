import requests
from django.core.management.base import BaseCommand

from stock.models import Stock


class Command(BaseCommand):
    help = "Load Stocks"

    def handle(self, *args, **options):
        # Fetches all Tickers Dump from NSE exchange
        def get_stock_data(exchange: str = "NSE"):
            url = "https://api.twelvedata.com/stocks"
            params = {"exchange": exchange}
            res = requests.get(url, params=params)
            return res.json()

        stocks_dict = get_stock_data().get("data", [])

        stock_objects = [
            Stock(symbol=stock_dict["symbol"], name=stock_dict["name"])
            for stock_dict in stocks_dict
        ]

        Stock.objects.bulk_create(stock_objects, ignore_conflicts=True)
