from rest_framework import serializers

from event_calendar.models import EventCalendar
from stock.serializers import SearchStockSerializer


class EventCalendarSerializer(serializers.ModelSerializer):
    symbol = SearchStockSerializer()

    class Meta:
        model = EventCalendar
        fields = [
            "id",
            "event_type",
            "symbol",
            "purpose",
            "description",
            "published_at",
            "attachment_url",
        ]
