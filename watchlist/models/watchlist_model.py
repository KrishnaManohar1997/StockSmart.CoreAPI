from django.db import models

from common.models import BaseModel
from user.models import User


class Watchlist(BaseModel):
    name = models.CharField(
        max_length=32, blank=True, null=True, default="My Watchlist"
    )
    created_by_user = models.OneToOneField(User, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "Watchlist"
        verbose_name_plural = "Watchlists"
        db_table = "Watchlist"
