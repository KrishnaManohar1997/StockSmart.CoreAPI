from django.db import models
from common.models import BaseModel


class News(BaseModel):
    class NewsAPISource(models.TextChoices):
        NEWS_API = "News API"
        SMALLCASE = "Smallcase"
        GOOGLE_RSS = "Google Rss"
        NONE = None

    title = models.CharField(max_length=512, unique=True, db_index=True)
    description = models.TextField(blank=False, null=False)
    api_source = models.CharField(
        max_length=16,
        choices=NewsAPISource.choices,
        blank=False,
        null=False,
        default=NewsAPISource.NONE,
    )
    source_name = models.CharField(max_length=64)
    source_id = models.CharField(max_length=32, null=True, blank=True)

    url = models.URLField(max_length=512, blank=False, null=False)
    image_url = models.URLField(max_length=356, blank=True, null=True)
    tickers = models.ManyToManyField("stock.stock")
    smallcases = models.ManyToManyField("smallcase.smallcase")
    published_at = models.DateTimeField()

    class Meta:
        db_table = "News"
        managed = True
        verbose_name = "News"
        verbose_name_plural = "News"
