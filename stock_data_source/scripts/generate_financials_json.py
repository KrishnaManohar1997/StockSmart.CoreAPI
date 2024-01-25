from stock.models import StockFinancial, Stock
import json

financials = list(StockFinancial.objects.prefetch_related("stock"))
financials_data = []


for f in financials:
    financials_data.append(
        {
            "statement": f.statement,
            "period": f.period,
            "data": f.data,
            "fiscal_date": str(f.fiscal_date),
            "stock": f.stock.symbol,
        }
    )


with open("financials_data.json", "w", encoding="utf-8") as f:
    json.dump(financials_data, f, ensure_ascii=False, indent=4)


stock_details = list(Stock.objects.all())
stock_details_data = []


for f in stock_details:
    stock_details_data.append(
        {
            "details": f.details,
            "statistics": f.statistics,
            "stock": f.symbol,
        }
    )


with open("stock_details_data.json", "w", encoding="utf-8") as f:
    json.dump(stock_details_data, f, ensure_ascii=False, indent=4)
