from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from common.models import BaseModel


class Report(BaseModel):
    message = models.TextField(default=None, blank=True, null=True)
    # the required fields to enable a generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField(editable=False, db_index=True)
    content_object = GenericForeignKey()

    class Meta:
        verbose_name = "Report"
        verbose_name_plural = "Reports"
        db_table = "Report"
