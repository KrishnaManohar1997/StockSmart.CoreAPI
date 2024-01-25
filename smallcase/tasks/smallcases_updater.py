import structlog

from stocksmart.celery import app
from smallcase.services import SmallcaseService

logger = structlog.getLogger("django.server")


@app.task(autoretry_for=(Exception,), retry_kwargs={"max_retries": 3, "countdown": 5})
def smallcases_updater():
    logger.info("Updating Smallcases Job Started")
    try:
        SmallcaseService().update_all_smallcases()
        logger.info("Updating Smallcases Job Executed Successfully")
    except Exception as error:
        logger.error(f"Updating Smallcases Job Failed --> {error}")
        raise Exception("Retrying the Job")
