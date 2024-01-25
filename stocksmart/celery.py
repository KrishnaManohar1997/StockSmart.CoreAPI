import os

from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stocksmart.settings")

app = Celery()
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.

app.config_from_object("django.conf:settings", namespace="CELERY")


# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    "update_user_karma_score": {
        "task": "user.tasks.user_karma_calculation.update_user_karma_score",
        # Scheduled to run at 6 AM and 6 PM
        "schedule": crontab(hour="6,18"),
    },
    "sync_trending_news": {
        "task": "news.tasks.sync_trending_news.sync_trending_news",
        # Scheduled to run at every 2 hours
        "schedule": crontab(minute=0, hour="*/2"),
    },
    "sync_nse_announcements": {
        "task": "event_calendar.tasks.sync_nse_announcements.sync_nse_announcements",
        # Every 15 mins from 6 AM to night 11 PM
        "schedule": crontab(minute="*/15", hour="6-23"),
    },
    "update_ticker_prices": {
        "task": "stock.tasks.update_ticker_prices_groww.update_ticker_prices",
        # Scheduled to Run everyday at 4:01 PM Weekdays only
        "schedule": crontab(hour="16", minute="01", day_of_week="1-5"),
    },
    "post_target_processor": {
        "task": "post.tasks.post_target_processor.post_target_processor",
        # Scheduled to Run everyday at 4:30 PM
        "schedule": crontab(hour="16", minute="30"),
    },
    "update_post_ticker_prices": {
        "task": "post.tasks.update_ticker_price_at_post_groww.update_ticker_price_at_post",
        # Scheduled to Run everyday at 1 PM
        "schedule": crontab(hour="1"),
    },
    "smallcases_updater": {
        "task": "smallcase.tasks.smallcases_updater.smallcases_updater",
        # Scheduled to Run everyday at 5:00 PM Weekdays only
        "schedule": crontab(hour="17", day_of_week="1-5"),
    },
}
