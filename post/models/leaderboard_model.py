from django.db import models

from common.models import BaseModel
from post.models import Post
from user.models import User


class Leaderboard(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.DO_NOTHING)
    percentage_change = models.DecimalField(
        blank=False, null=False, max_digits=8, decimal_places=2
    )
    signal_type = models.CharField(max_length=16, blank=False, null=False)
    date = models.DateField(blank=False, null=False)
    position = models.PositiveIntegerField(blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    reward = models.IntegerField(blank=False, null=False)

    created_by_user = None

    class Meta:
        db_table = "Leaderboard"
        managed = True
        verbose_name = "Leaderboard"
        verbose_name_plural = "Leaderboard"
