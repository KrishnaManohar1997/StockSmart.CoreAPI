from rest_framework import serializers

from stock.models import Stock


class SearchStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ["id", "name", "symbol"]


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ["name", "symbol"]
