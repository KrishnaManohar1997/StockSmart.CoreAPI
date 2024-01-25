import requests

from queue import Queue
from threading import Thread

import requests
from stock.models import Stock

symbols = list(Stock.objects.all().values_list("symbol", flat=True))
q = Queue(len(symbols))
num_threads = 5
tickerTapeDetails = []


session = requests.Session()


def get_stock_details_by_symbol(symbol):
    try:
        response = session.get(f"https://api.tickertape.in/external/oembed/{symbol}")
        if response.status_code == 200:
            return response.json()["data"]
    except Exception as e:
        print(f"Error for {symbol} - {e}")
    return None


def do_stuff(q):
    while True:
        symbol = q.get()
        print("processing ", symbol)
        data = get_stock_details_by_symbol(symbol)
        if data:
            tickerTapeDetails.append(data)
        q.task_done()


for i in range(num_threads):
    worker = Thread(target=do_stuff, args=(q,))
    worker.start()

for x in symbols:
    q.put(x)

try:
    q.join()
except Exception as e:
    print(e)

import json

with open("tickertapeDetails.json", "w") as fp:
    json.dump(tickerTapeDetails, fp, indent=4)
