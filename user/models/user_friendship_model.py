from django.db import models

from common.models import BaseModel

from . import User


class UserFriendship(BaseModel):
    relating_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="relating_friendships"
    )
    related_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="related_friendships"
    )

    class UserFriendshipType(models.TextChoices):
        NO_FRIENDSHIP = None
        FOLLOW = "Follow"
        BLOCKED = "Blocked"
        UNBLOCK = "Unblock"

    friendship = models.CharField(
        max_length=16,
        blank=False,
        null=False,
        choices=UserFriendshipType.choices,
        default=UserFriendshipType.NO_FRIENDSHIP,
    )

    class Meta:
        unique_together = ("relating_user", "related_user")
        verbose_name = "UserFriendship"
        verbose_name_plural = "UserFriendships"
        db_table = "User_Friendship"
