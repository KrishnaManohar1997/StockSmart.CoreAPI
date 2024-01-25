from notification.models import Notification
import django.utils.timezone as dj_datetime


class NotificationRepository:
    def get_user_notifications(self, user):
        return (
            user.notifications.all().order_by("-created_at").prefetch_related("sender")
        )

    def get_unread_notifications_count(self, user):
        unread_notifications = user.notifications.filter(read_at__isnull=True)
        if user.last_notification_read_at:
            return unread_notifications.filter(
                created_at__gte=user.last_notification_read_at
            ).count()
        return unread_notifications.count()

    def get_recent_read_notification(self, user):
        return (
            user.notifications.filter(read_at__isnull=False)
            .order_by("-created_at")
            .prefetch_related("sender")
            .first()
        )

    def get_recent_user_notification(self, user):
        return user.notifications.order_by("-created_at").first()

    def mark_user_notifications_read(self, user):
        user.last_notification_read_at = dj_datetime.now()
        user.save()
        return True

    def get_notification_by_id(self, notification_id):
        return Notification.objects.filter(id=notification_id).first()

    def mark_notification_read(self, notification):
        notification.read_at = dj_datetime.now()
        notification.save()
        return notification

    def bulk_create_notifications(self, notifications):
        return Notification.objects.bulk_create(notifications)
