from rest_framework import serializers
from user.serializers.user_notification_serializer import UserNotificationSerializer
from notification.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    sender = UserNotificationSerializer()

    class Meta:
        model = Notification
        fields = ["id", "sender", "read_at", "data", "created_at", "event"]


class CreateNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["sender", "receiver", "data", "event"]
