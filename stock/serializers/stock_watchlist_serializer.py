from rest_framework import serializers

from stock.models import Stock


class StockWatchlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ["name", "symbol", "ratios"]
