import requests

# Fetches all Tickers Dump from NSE exchange
def get_stock_data(exchange: str = "NSE"):
    url = "https://api.twelvedata.com/stocks"
    params = {"exchange": exchange}
    res = requests.get(url, params=params)
    return res.json()
