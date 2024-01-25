from django.urls import path

from notification.views import (
    UserNotificationView,
    ReadAllUserNotificationView,
    ReadUserNotificationView,
)

# v1/notifications/
urlpatterns = [
    # v1/notifications/
    path("", UserNotificationView.as_view()),
    # v1/notifications/read/
    path("read/", ReadAllUserNotificationView.as_view()),
    # v1/notifications/<notification_id>/read/
    path("<str:notification_id>/read/", ReadUserNotificationView.as_view()),
]
