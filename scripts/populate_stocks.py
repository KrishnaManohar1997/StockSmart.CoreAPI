import csv

from stock.serializers import StockSerializer


def serialize_stock_data(stock_list):
    try:
        serialized_data = StockSerializer(data=stock_list, many=True)
        if not serialized_data.is_valid():
            print("Following errors Occurred")
            print(stock_list)
            print(serialized_data.errors)
        else:
            serialized_data.save()
    except Exception as error:
        print(error)


with open(r"D:\projects\StockSmart.CoreAPI\scripts\EQUITY_L.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    line_count = 0
    stock_data_list = list()
    for row in csv_reader:

        if line_count == 0:
            pass
        else:
            stock_data_list.append(
                {"symbol": row[0], "name": row[1], "last_traded_at_price": row[7]}
            )
        line_count += 1
        if line_count % 10 == 0:
            print("Processing batch")
            serialize_stock_data(stock_data_list)
            stock_data_list = []
    serialize_stock_data(stock_data_list)
    print("Stocks Data ingested successfully")
