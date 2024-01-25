import structlog

from news.services.news_service import NewsService
from stocksmart.celery import app

logger = structlog.getLogger("django.server")


@app.task()
def sync_trending_news():
    logger.info("Syncing Trending News Job Started")
    try:
        NewsService().fetch_and_update_trending_news()
        logger.info("Syncing Trending News Job Ended")
    except Exception as error:
        logger.error(f"Syncing Trending News Job Failed --> {error}")
