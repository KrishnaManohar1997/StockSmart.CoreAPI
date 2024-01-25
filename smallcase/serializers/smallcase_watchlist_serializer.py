from rest_framework import serializers

from smallcase.models import Smallcase


class SmallcaseWatchlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Smallcase
        fields = [
            "symbol",
            "name",
            "returns",
            "index_value",
            "price_52_week_high",
            "price_52_week_low",
        ]
