from rest_framework import serializers

from stock.models import StockFinancial


class StockFinancialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockFinancial
        fields = [
            "period",
            "fiscal_date",
            "data",
            "statement",
        ]
