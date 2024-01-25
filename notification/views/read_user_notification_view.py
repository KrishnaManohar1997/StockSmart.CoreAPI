from common.base_view import BaseView
from notification.services import NotificationService


class ReadAllUserNotificationView(BaseView):
    notification_service = NotificationService()

    def get(self, request):
        try:
            self.notification_service.mark_user_notifications_read(request.user)
            return self.success_response("Ok")
        except Exception:
            return self.bad_request_response("Failed to Read")


class ReadUserNotificationView(BaseView):
    notification_service = NotificationService()

    def get(self, request, notification_id):
        try:
            self.notification_service.mark_notification_read(
                notification_id, str(request.user.id)
            )
            return self.success_response("Ok")
        except Exception as error:
            print(error)
            return self.bad_request_response("Failed to Read")
