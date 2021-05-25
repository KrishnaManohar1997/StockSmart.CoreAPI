from django.db import models

from common.models import BaseModel


class Post(BaseModel):
    class SignalType(models.TextChoices):
        BULLISH = "Bullish"
        BEARISH = "Bearish"

    signal_type = models.CharField(
        max_length=16, choices=SignalType.choices, blank=False, null=False
    )
    content = models.CharField(max_length=512, blank=False, null=False)
    signal_end_at = models.DateTimeField(blank=False, null=False)

    class Meta:
        db_table = "Post"
        managed = True
        verbose_name = "Post"
        verbose_name_plural = "Posts"
