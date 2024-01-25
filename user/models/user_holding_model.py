from django.db import models

from common.models import BaseModel
from user.models import User


class UserHolding(BaseModel):
    holdings = models.JSONField(blank=False, null=False)
    user = models.OneToOneField(User, blank=False, null=False, on_delete=models.CASCADE)
    last_update = models.DateTimeField(blank=False, null=False)
    broker_name = models.CharField(
        max_length=32, null=False, blank=False, db_index=True
    )

    class Meta:
        db_table = "UserHolding"
        managed = True
        verbose_name = "UserHolding"
        verbose_name_plural = "UserHoldings"
