from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from gm2m import GM2MField

from common.models import BaseModel
from post.helpers.post_mentions_json_schema import get_post_mentions_schema


class Post(BaseModel):
    class SignalType(models.TextChoices):
        BULLISH = "Bullish"
        BEARISH = "Bearish"
        NEUTRAL = None

    signal_type = models.CharField(
        max_length=16,
        default=SignalType.NEUTRAL,
        choices=SignalType.choices,
        blank=True,
        null=True,
    )
    content = models.CharField(max_length=1024, blank=False, null=False)
    url = models.CharField(
        max_length=128, blank=False, null=False, unique=True, db_index=True
    )
    media = models.URLField(blank=True, null=True)
    # Counter for Likes and Comments
    reaction_count = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)
    mentions = models.JSONField(
        default=get_post_mentions_schema, null=False, blank=False
    )
    reactions = GenericRelation("Reaction")
    comments = GenericRelation("Comment")
    source = models.JSONField(blank=False, null=False)

    # Ticker Mentioned in Posts
    ticker_mentions = GM2MField(
        "stock.Stock", "smallcase.Smallcase", through="mentions.PostTickerMention"
    )
    # User Mentions
    user_mentions = models.ManyToManyField(
        "user.User",
        related_name="post_mentions",
        through="mentions.PostUserMention",
        through_fields=(
            "post",
            "mentioned_user",
        ),
    )

    # Post Target Related Fields
    ticker_mkt_price_at_post = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True
    )
    ticker_mkt_price_at_target = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True
    )
    target_price = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True
    )
    signal_expire_at = models.DateField(blank=True, null=True)
    is_target_reached = models.BooleanField(default=None, blank=True, null=True)

    class Meta:
        db_table = "Post"
        managed = True
        verbose_name = "Post"
        verbose_name_plural = "Posts"
