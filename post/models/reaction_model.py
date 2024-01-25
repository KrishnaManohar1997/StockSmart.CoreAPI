from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from common.models import BaseModel


class Reaction(BaseModel):
    class ReactionType(models.TextChoices):
        LIKE = "Like"
        REMOVE_REACTION = "RemoveReaction"

    reaction = models.CharField(
        max_length=16,
        default=ReactionType.LIKE,
        choices=ReactionType.choices,
        blank=False,
        null=False,
    )
    # the required fields to enable a generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField(editable=False, db_index=True)
    content_object = GenericForeignKey()

    class Meta:
        db_table = "Reaction"
        managed = True
        verbose_name = "Reaction"
        verbose_name_plural = "Reactions"
        unique_together = ("object_id", "created_by_user_id")
