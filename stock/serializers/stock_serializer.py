from rest_framework import serializers
from stock.models import Stock


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = [
            "id",
            "is_deleted",
            "name",
            "symbol",
            "last_traded_at_price",
            "category",
            "type",
        ]
