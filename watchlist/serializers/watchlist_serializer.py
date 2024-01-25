from rest_framework import serializers
from django.core.exceptions import ValidationError
from stock.serializers import StockWatchlistSerializer
from smallcase.serializers import SmallcaseWatchlistSerializer
from watchlist.models import Watchlist, WatchlistItem


class WatchlistRelatedObjectSerializer(serializers.RelatedField):
    def to_representation(self, value):
        class_name = value.__class__.__name__
        if class_name == "Stock":
            data = StockWatchlistSerializer(value).data
        elif class_name == "Smallcase":
            data = SmallcaseWatchlistSerializer(value).data
        else:
            raise ValidationError("Unexpected type of Watchlist object", code=500)
        data.update({"type": class_name})
        return data


class WatchlistItemSerializer(serializers.ModelSerializer):
    item = WatchlistRelatedObjectSerializer(read_only=True, source="content_object")

    class Meta:
        model = WatchlistItem
        fields = ["id", "item"]


class AddWatchlistItemSerializer(serializers.ModelSerializer):
    object_id = serializers.UUIDField(required=True)

    class Meta:
        model = WatchlistItem
        fields = [
            "created_by_user",
            "object_id",
            "watchlist",
        ]
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=("object_id", "created_by_user"),
                message=("Already watchlisted"),
            )
        ]
