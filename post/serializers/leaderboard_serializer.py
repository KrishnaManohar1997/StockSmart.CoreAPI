from rest_framework import serializers

from post.models import Leaderboard

from user.serializers import CommentUserSerializer
from post.serializers import PostDetailsSerializer, PostNotificationSerializer


class LeaderboardSerializer(serializers.ModelSerializer):
    user = CommentUserSerializer()
    post = PostDetailsSerializer()

    class Meta:
        model = Leaderboard
        fields = ["user", "post", "percentage_change", "position", "signal_type"]


class LeaderboardNotificationSerializer(serializers.ModelSerializer):
    post = PostNotificationSerializer()

    class Meta:
        model = Leaderboard
        fields = [
            "post",
            "percentage_change",
            "position",
            "signal_type",
            "date",
            "reward",
        ]
