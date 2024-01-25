from rest_framework import serializers

from post.models import Post

from user.serializers import CommentUserSerializer


class PostFeedSerializer(serializers.ModelSerializer):
    created_by_user = CommentUserSerializer()

    class Meta:
        model = Post
        fields = [
            "id",
            "content",
            "media",
            "signal_type",
            "url",
            "created_by_user",
            "reaction_count",
            "comment_count",
            "mentions",
            "created_at",
            "source",
            "target_price",
            "signal_expire_at",
            "ticker_mkt_price_at_post",
            "ticker_mkt_price_at_target",
            "is_target_reached",
        ]


class PostDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "signal_type", "url", "source"]


class PostNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "content", "url", "source"]


class PostTargetNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "id",
            "content",
            "url",
            "source",
            "is_target_reached",
            "signal_type",
            "ticker_mkt_price_at_post",
            "ticker_mkt_price_at_target",
            "target_price",
            "created_by_user_id",
        ]
