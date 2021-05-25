from django.db import models
from django.db.models.deletion import DO_NOTHING
from . import Post
from stock.models import Stock
from common.models import BaseModel


class PostStockMention(BaseModel):
    post = models.ForeignKey(Post, on_delete=DO_NOTHING, related_name="posts")
    stock = models.ForeignKey(Stock, on_delete=DO_NOTHING, related_name="stocks")

    class Meta:
        db_table = "Post_StockMention"
        managed = True
        verbose_name = "Post_StockMention"
        verbose_name_plural = "Post_StockMentions"
