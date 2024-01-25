import json
from uuid import UUID

import pandas as pd

from stock.models import Stock, StockFinancial


def is_valid_uuid(value):
    try:
        UUID(value)
        return True
    except:
        return False


symbol_id_map = dict(Stock.objects.values_list("symbol", "id"))

df = pd.read_json("financials_data.json")

print(df.head())
print("Mapping Stock Id based on Stock Symbol")

for symbol, id in symbol_id_map.items():
    df.loc[df["stock"] == symbol, "stock"] = str(id)

df = df.rename(columns={"stock": "stock_id"})


json_list = json.loads(json.dumps(list(df.T.to_dict().values())))


sf_obj = []

for dic in json_list:
    uid = dic.get("stock_id", None)
    if not uid or not is_valid_uuid(uid):
        continue
    sf_obj.append(StockFinancial(**dic))

StockFinancial.objects.bulk_create(sf_obj, batch_size=500)
# ---------------------------------------------------------------------------


details_df = pd.read_json("stock_details_data.json")


json_list = json.loads(json.dumps(list(details_df.T.to_dict().values())))


symbol_stock_map = {s.symbol: s for s in Stock.objects.all()}

so_obj = []

for dic in json_list:
    stock = symbol_stock_map.get(dic.get("stock"))
    if not stock:
        continue
    stock.statistics = dic.get("statistics")
    stock.details = dic.get("details")
    so_obj.append(stock)


Stock.objects.bulk_update(so_obj, fields=["statistics", "details"], batch_size=500)
