import structlog

from event_calendar.services import EventCalendarService
from stocksmart.celery import app

logger = structlog.getLogger("django.server")


@app.task()
def sync_nse_announcements():
    logger.info("Syncing NSE announcements from RSS Job Started")
    try:
        EventCalendarService().sync_nse_announcements_rss()
        logger.info("Syncing NSE announcements from RSS Job Ended Successfully")
    except Exception as error:
        logger.error(f"Syncing NSE announcements from RSS Job Failed --> {error}")
