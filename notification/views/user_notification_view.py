from common.base_view import BaseView
from notification.serializers import NotificationSerializer
from notification.services import NotificationService
from rest_framework.pagination import LimitOffsetPagination


class UserNotificationView(BaseView):
    notification_service = NotificationService()
    serializer = NotificationSerializer
    paginator = LimitOffsetPagination()

    def get(self, request):
        notifications = self.notification_service.get_user_notifications(request.user)
        paginated_notifications = self.paginator.paginate_queryset(
            notifications, request
        )
        notifications_data = self.serializer(paginated_notifications, many=True).data
        payload = {
            "last_read_at": request.user.last_notification_read_at,
            "unread_count": self.notification_service.get_unread_notifications_count(
                request.user
            ),
            "notifications": notifications_data,
        }
        if not notifications_data:
            return self.empty_paginated_response("No notifications")
        return self.paginated_response(
            self.paginator, message="Notifications", data=payload
        )
