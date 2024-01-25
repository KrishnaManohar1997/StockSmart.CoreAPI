from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from common.models import BaseModel
from post.models import Post


class PostTickerMention(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.DO_NOTHING)
    watchlisted_market_price = models.DecimalField(
        blank=False, null=False, default=0, max_digits=10, decimal_places=2
    )
    ticker = GenericForeignKey(ct_field="ticker_type", fk_field="ticker_id")
    ticker_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    ticker_id = models.UUIDField(editable=False, db_index=True)

    class Meta:
        unique_together = ("post", "ticker_id")
        verbose_name = "Post_Ticker_Mention"
        verbose_name_plural = "Post Ticker Mentions"
        db_table = "Post_Ticker_Mention"
