import structlog
from notification.services.notification_service import NotificationService

from stocksmart.celery import app
from user.models import User
from user.services import UserService

logger = structlog.getLogger("django.server")


def calculate_success_rate_for_user(user):
    prev_success_rate = user.success_rate
    user_targets = list(
        (
            UserService()
            .get_user_created_posts(user)
            .exclude(is_target_reached=None)
            .values_list("is_target_reached", flat=True)
        )
    )
    total_targets = len(user_targets)
    if total_targets != 0:
        user.success_rate = round((user_targets.count(True) / total_targets) * 100)
    if user.success_rate != prev_success_rate:
        NotificationService().send_user_success_rate_notification(
            user.id, prev_success_rate, user.success_rate
        )
    return user


@app.task(autoretry_for=(Exception,), retry_kwargs={"max_retries": 3, "countdown": 5})
def user_success_rate_updater(user_ids):
    logger.info("User Success Rate Updating Job Started")
    users = list(UserService().get_users_by_ids(user_ids))
    try:
        User.objects.bulk_update(
            list(map(calculate_success_rate_for_user, users)), ["success_rate"]
        )
        logger.info("User Success Rate Updating Job Ended")
    except Exception as error:
        logger.error(f"User Success Rate Updating Job Failed --> {error}")
        raise Exception("Retrying the Job")
