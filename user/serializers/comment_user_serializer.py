from rest_framework import serializers

from user.models import User


class CommentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "username",
            "profile_picture_url",
            "karma",
            "success_rate",
            "verified_professional_accounts",
        ]
