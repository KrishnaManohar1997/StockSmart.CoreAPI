from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models

from common.models import BaseModel


class Comment(BaseModel):
    text = models.CharField(max_length=512, blank=False, null=False)
    reaction_count = models.PositiveIntegerField(default=0)
    reactions = GenericRelation("Reaction")
    # the required fields to enable a generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField(editable=False, db_index=True)
    content_object = GenericForeignKey()

    class Meta:
        db_table = "Comment"
        managed = True
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
