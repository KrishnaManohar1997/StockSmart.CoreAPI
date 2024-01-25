from rest_framework import serializers

from user.models import User


class UserNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "username", "profile_picture_url"]
