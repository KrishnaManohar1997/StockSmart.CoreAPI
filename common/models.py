import uuid

from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_by_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="%(class)s_created_by",
        on_delete=models.CASCADE,
        default=None,
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True


class SignupMethod(models.TextChoices):
    SIMPLE = "Simple"
    GOOGLE = "Google"
    TWITTER = "Twitter"


class BaseStockModel(BaseModel):
    symbol = models.CharField(
        max_length=32, blank=False, null=False, db_index=True, unique=True
    )
    name = models.CharField(max_length=128, blank=False, null=False, db_index=True)
    last_news_fetched_at = models.DateTimeField(blank=True, null=True, default=None)
    latest_pub_news_date = models.DateTimeField(blank=True, null=True, default=None)
    logo_url = models.URLField(blank=True, null=True)
    # Ticker watchlisted
    watchlist_item = GenericRelation("watchlist.WatchlistItem")

    class Meta:
        abstract = True
