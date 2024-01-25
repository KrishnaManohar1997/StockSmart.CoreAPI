from django.db import models
from user.models import User
from common.models import BaseModel
from notification.constants import NotificationIntent

from pydantic import BaseModel as PydanticBaseModel


class KarmaChangeEvent(PydanticBaseModel):
    prev_karma: int
    new_karma: int


class SuccessRateChange(PydanticBaseModel):
    prev_success_rate: int
    new_success_rate: int


class Notification(BaseModel):
    created_by_user = None
    receiver = models.ForeignKey(
        User,
        blank=False,
        null=False,
        related_name="notifications",
        on_delete=models.CASCADE,
    )
    sender = models.ForeignKey(
        User,
        blank=True,
        null=True,
        related_name="notifications_sent",
        on_delete=models.CASCADE,
    )
    event = models.CharField(
        max_length=32,
        choices=NotificationIntent.choices,
        blank=False,
        null=False,
    )
    read_at = models.DateTimeField(blank=True, null=True)
    data = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = "Notification"
        managed = True
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
