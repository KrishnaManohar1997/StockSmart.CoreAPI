from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from common.models import BaseModel
from watchlist.models.watchlist_model import Watchlist


class WatchlistItem(BaseModel):
    watchlist = models.ForeignKey(
        Watchlist, on_delete=models.DO_NOTHING, related_name="watchlist_items"
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField(editable=False, db_index=True)
    content_object = GenericForeignKey()

    class Meta:
        unique_together = ("created_by_user_id", "object_id")
        verbose_name = "Watchlist_Item"
        verbose_name_plural = "Watchlist_Items"
        db_table = "Watchlist_Item"
