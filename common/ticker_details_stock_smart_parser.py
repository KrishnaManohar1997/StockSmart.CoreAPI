import json

from stock.models import Stock
from stock.models.stock_model import get_allowed_ratios_fields


def get_ss_format(ticker_tape_details):
    tt_ratios = ticker_tape_details["ratios"]
    ratios = {}
    for key in get_allowed_ratios_fields():
        ratios[key] = tt_ratios.pop(key, "")
    return {
        "sector": ticker_tape_details.get("info", {}).get("sector", {}),
        "ratios": ratios,
    }


data = json.loads(open("tickerDetails.json").read())
stock_objs = []
for d in data:
    symbol = d["info"]["ticker"]
    try:
        print("Processing - ", symbol)
        stock = Stock.objects.get(symbol=symbol)
        for (key, value) in get_ss_format(d).items():
            setattr(stock, key, value)
        stock_objs.append(stock)
    except Stock.DoesNotExist:
        print("Stock Doesn't exist", symbol)
    except Exception as e:
        print("Error parsing Data ", symbol, " --- ", e)

Stock.objects.bulk_update(stock_objs, get_ss_format(data[0]).keys())
print("Completed Storing data on Stocks")
