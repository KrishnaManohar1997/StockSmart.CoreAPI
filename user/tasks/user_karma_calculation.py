import structlog
from django.db.models import Sum

from common.constants.karma_bonus_intent import KarmaBonusIntent
from notification.services.notification_service import NotificationService
from stocksmart.celery import app
from user.models import User
from user.services import UserService

logger = structlog.getLogger("django.server")


def calculate_karma_for_user(user):
    user_karma = 0
    if user.is_broker_connected():
        user_karma += KarmaBonusIntent.BROKER_CONNECT.value
        user_karma += (
            KarmaBonusIntent.AUTHORIZE_HOLDINGS_IMPORT.value
            if user.is_import_holdings_authorized()
            else 0
        )
    user_karma += (
        user.post_created_by.aggregate(Sum("reaction_count"))["reaction_count__sum"]
        or 0
    )
    user_karma += (
        user.comment_created_by.aggregate(Sum("reaction_count"))["reaction_count__sum"]
        or 0
    )
    user_karma += (
        KarmaBonusIntent.IS_VERIFIED_PROFESSIONAL.value
        if user.verified_professional_accounts
        else 0
    )
    if user.karma != user_karma:
        NotificationService.send_user_karma_notification(
            user.id, user.karma, user_karma
        )
    user.karma = user_karma
    return user


@app.task()
def update_user_karma_score():
    logger.info("User Karma Updating Job Started")
    users = list(UserService().get_all_users())
    try:
        User.objects.bulk_update(list(map(calculate_karma_for_user, users)), ["karma"])
        logger.info("User Karma Updating Job Ended")
    except Exception as error:
        logger.error(f"User Karma Updating Job Failed --> {error}")
