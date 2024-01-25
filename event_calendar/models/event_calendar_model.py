from django.db import models

from common.models import BaseModel


class EventCalendar(BaseModel):
    class EventType(models.TextChoices):
        NSE_HOLIDAY = "NSE Holiday"
        NSE_NON_WORKING_DAY = "Non Working Day"
        NSE_TICKER_RESULT = "NSE Ticker Result"
        NSE_TICKER_EVENT = "NSE Ticker Event"
        NSE_TICKER_ANNOUNCEMENT = "NSE Ticker Announcement"

    symbol = models.ForeignKey(
        "stock.stock", blank=False, null=False, on_delete=models.DO_NOTHING
    )
    event_type = models.CharField(
        max_length=32,
        blank=False,
        null=False,
        db_index=True,
        choices=EventType.choices,
    )
    published_at = models.DateTimeField(blank=False, null=False)
    description = models.TextField()
    purpose = models.TextField()
    attachment_url = models.URLField(blank=True, null=True)
    event_data = models.JSONField(default=dict, blank=True, null=True)
    source_id = models.CharField(max_length=16, unique=True, null=True, blank=True)

    class Meta:
        unique_together = ("symbol", "event_type", "published_at")
        verbose_name = "Event_Calendar"
        verbose_name_plural = "Event_Calendar"
        db_table = "Event_Calendar"
