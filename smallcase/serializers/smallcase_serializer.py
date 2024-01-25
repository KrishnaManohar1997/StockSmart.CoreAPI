from rest_framework import serializers

from smallcase.models import Smallcase


class CreateSmallcaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Smallcase
        fields = [
            "symbol",
            "name",
            "last_news_fetched_at",
            "latest_pub_news_date",
            "logo_url",
            "price_52_week_high",
            "price_52_week_low",
            "publisher_name",
            "description",
            "last_rebalanced",
            "risk_label",
            "risk_percentage",
            "minimum_investment",
            "constituents",
            "returns",
            "cagr",
            "index_value",
        ]


class AllSmallcaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Smallcase
        fields = [
            "id",
            "symbol",
            "name",
            "logo_url",
            "cagr",
            "minimum_investment",
            "description",
            "publisher_name",
        ]


class SmallcaseDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Smallcase
        fields = [
            "id",
            "symbol",
            "name",
            "logo_url",
            "price_52_week_high",
            "price_52_week_low",
            "publisher_name",
            "description",
            "last_rebalanced",
            "risk_label",
            "risk_percentage",
            "minimum_investment",
            "constituents",
            "returns",
            "cagr",
            "index_value",
        ]


class AnonymousUserSmallcaseDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Smallcase
        fields = [
            "id",
            "symbol",
            "name",
            "logo_url",
            "price_52_week_high",
            "price_52_week_low",
            "publisher_name",
            "description",
            "last_rebalanced",
            "risk_label",
            "risk_percentage",
            "minimum_investment",
            "returns",
            "cagr",
            "index_value",
        ]
