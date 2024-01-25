from __future__ import absolute_import
from .celery import app as celery_app
from common.helper.logging_utils import configure_structlog

configure_structlog()

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.

__all__ = ("celery_app",)
