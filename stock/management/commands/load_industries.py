import requests
from django.core.management.base import BaseCommand

from stock.models import Stock


class Command(BaseCommand):
    help = "Load Industry of Stocks"

    def handle(self, *args, **options):
        # Fetches Sectors for Each Stock and save it
        def get_stock_industries():
            """
            [{
                "SCRIP_CD": "500002",
                "Scrip_Name": "ABB India Limited",
                "Status": "Active",
                "GROUP": "A",
                "FACE_VALUE": "2.00",
                "ISIN_NUMBER": "INE117A01022",
                "INDUSTRY": "Heavy Electrical Equipment",
                "scrip_id": "ABB",
                "Segment": "Equity",
                "NSURL": "https://www.bseindia.com/stock-share-price/abb-india-limited/abb/500002/",
                "Issuer_Name": "ABB India Limited"
            }]
            """
            url = "https://api.bseindia.com/BseIndiaAPI/api/ListofScripData/w?Group=&Scripcode=&industry=&segment=Equity&status=Active"
            return requests.get(url).json()

        try:
            stocks_dict = get_stock_industries()
        except Exception:
            print(
                """Please visit https://www.bseindia.com/corporates/List_Scrips.html in your browser
                Select Segment -> Equity 
                and Status -> Active and Submit, Once the data appears there
                then try the Command again"""
            )
            exit()
        print("Received JSON data of Tickers", stocks_dict[:2], "... Truncated data")
        industry_list = {}
        print("Parsing Stock data for Industries")
        for stock_dict in stocks_dict:
            industry = stock_dict["INDUSTRY"]
            symbol = stock_dict["scrip_id"]
            if industry not in industry_list:
                industry_list[industry] = [symbol]
            else:
                industry_list[industry].append(symbol)

        for industry, stock_symbols in industry_list.items():
            if industry != "":
                print(f"Updating Tickers for {industry=}")
                Stock.objects.filter(symbol__in=stock_symbols).update(industry=industry)
        Stock.objects.filter(industry=None).update(industry="Miscellaneous")
