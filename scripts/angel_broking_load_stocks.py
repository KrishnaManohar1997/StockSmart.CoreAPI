from itertools import islice
from stock.models import Stock
import json


# Stock.objects.all().delete()
# {
#     "token": "2885",
#     "symbol": "RELIANCE-EQ",
#     "name": "RELIANCE",
#     "expiry": "",
#     "strike": "-1.000000",
#     "lotsize": "1",
#     "instrumenttype": "",
#     "exch_seg": "nse_cm",
#     "tick_size": "5.000000",
# }
JSON_PATH = r"D:\Stocksmart\Scripts\stocks_dump.json"
with open(JSON_PATH) as f:
    data = json.load(f)

objs = []
for i in data:
    if i["exch_seg"] == "BSE" and i["expiry"] in ["", None]:
        objs.append(Stock(symbol=i["symbol"], token=i["token"], name=i["name"]))

batch_size = 15000
while True:
    batch = list(islice(objs, batch_size))
    if not batch:
        break
    Stock.objects.bulk_create(batch, batch_size, ignore_conflicts=True)
