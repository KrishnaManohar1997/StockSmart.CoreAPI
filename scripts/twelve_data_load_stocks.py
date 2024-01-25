from stock.models import Stock
from StocksTwelveData import get_stock_data

stocks_dict = get_stock_data().get("data", [])

stock_objects = [
    Stock(symbol=stock_dict["symbol"], name=stock_dict["name"])
    for stock_dict in stocks_dict
]

Stock.objects.bulk_create(stock_objects, ignore_conflicts=True)
