from rest_framework import serializers

from stock.models import Stock


class StockDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = [
            "id",
            "name",
            "symbol",
            "industry",
            "sector",
            "ratios",
            "ltp",
            "prev_ltp",
        ]


class StockOverviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ["id", "name", "symbol", "industry", "sector", "details", "statistics"]
