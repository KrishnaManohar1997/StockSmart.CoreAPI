from rest_framework import serializers

from user.models import User
from user.services import UserFriendshipService


class PublicUserSerializer(serializers.ModelSerializer):
    is_reported = serializers.SerializerMethodField()
    friendship_status = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "date_joined",
            "is_reported",
            "friendship_status",
            "name",
            "username",
            "karma",
            "about",
            "profile_picture_url",
            "success_rate",
            "verified_professional_accounts",
            "followers_count",
            "following_count",
        ]

    def get_is_reported(self, obj):
        requesting_user = self.context["request"].user
        return obj.reports.filter(
            created_by_user=requesting_user, object_id=obj.id
        ).exists()

    def get_friendship_status(self, obj):
        requesting_user = self.context["request"].user
        user_friendship = UserFriendshipService().get_user_friendship_or_none(
            requesting_user.id, obj.id
        )
        if user_friendship:
            return user_friendship.friendship
        return user_friendship
