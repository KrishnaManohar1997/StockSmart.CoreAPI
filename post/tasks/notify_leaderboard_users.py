# This worker helps in notifying users about their Leaderboard Positions

import structlog
from django.conf import settings

from common.constants import get_ss_user_ids
from common.helper import EmailService, EmailTemplate
from common.helper.datetime_helper import DateTimeHelper
from notification.services import NotificationService
from post.services import LeaderboardService
from stocksmart.celery import app
from user.models.user_model import User

logger = structlog.getLogger("django.server")


@app.task(autoretry_for=(Exception,), retry_kwargs={"max_retries": 3, "countdown": 5})
def notify_leaderboard_users():
    logger.info("Notifying Leaderboard Users Job Started")
    try:
        today, _ = DateTimeHelper.get_today_start_and_end()
        send_leaderboard_notification = (
            NotificationService().leaderboard_winner_notification
        )
        leaderboard_queryset = LeaderboardService().get_leaderboard_on_date(
            today.date()
        )
        for leaderboard_obj in leaderboard_queryset:
            # Send App native Notification
            send_leaderboard_notification(leaderboard_obj)

            # Email Notification
            leaderboard_details = {
                "name": leaderboard_obj.user.name,
                "position": leaderboard_obj.position,
                "percentage_change": leaderboard_obj.percentage_change,
                "signal_type": leaderboard_obj.signal_type,
                "ticker_symbol": leaderboard_obj.post.source.get("symbol"),
            }
            # EmailService.send_template.delay(
            #     settings.SS_FROM_EMAIL,
            #     [leaderboard_obj.user.email],
            #     EmailTemplate.LEADERBOARD_WINNER_EMAIL,
            #     merge_variables=leaderboard_details,
            # )
            logger.info("Notifying Leaderboard Users Job Executed Successfully")
        if not leaderboard_queryset:
            return
        leaderboard_users_list = list(
            leaderboard_queryset.values_list("user_id", flat=True)
        )
        exclude_user_ids = []
        exclude_user_ids.extend(leaderboard_users_list)
        exclude_user_ids.extend(get_ss_user_ids(settings.APP_ENVIRONMENT))

        non_leaderboard_user_emails = list(
            User.objects.exclude(id__in=exclude_user_ids).values_list(
                "email", flat=True
            )
        )
        # if settings.APP_ENVIRONMENT == "PRODUCTION":
        #     EmailService.send_template.apply_async(
        #         args=[
        #             settings.SS_FROM_EMAIL,
        #             non_leaderboard_user_emails,
        #             EmailTemplate.LEADERBOARD_RESULTS_EMAIL,
        #         ],
        #         countdown=900,
        #     )

        NotificationService.leaderboard_results_notification(
            list(
                User.objects.exclude(id__in=leaderboard_users_list).values_list(
                    "id", flat=True
                )
            )
        )
        logger.info("Notifying All Users for Leaderboard Results Executed Successfully")
    except Exception as error:
        logger.info(f"Notifying Leaderboard Users Job Failed --> {error}")
