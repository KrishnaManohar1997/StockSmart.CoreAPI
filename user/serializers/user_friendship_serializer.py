from rest_framework import serializers

from user.models import User, UserFriendship


class FollowerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "username", "profile_picture_url"]


class UserFriendshipFollowerSerializer(serializers.ModelSerializer):
    follower = FollowerUserSerializer(source="relating_user")

    class Meta:
        model = UserFriendship
        fields = ["follower"]


class UserFriendshipFollowingSerializer(serializers.ModelSerializer):
    following_user = FollowerUserSerializer(source="related_user")

    class Meta:
        model = UserFriendship
        fields = ["following_user"]
