from rest_framework import serializers
from common.helper.text_sanitizer import sanitize_text

from post.models import Comment
from user.serializers import CommentUserSerializer


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["text"]

    def validate(self, data):
        data["text"] = sanitize_text(data["text"]).strip()
        return data


class CommentsViewSerializer(serializers.ModelSerializer):
    created_by_user = CommentUserSerializer()

    class Meta:
        model = Comment
        fields = ["id", "text", "created_by_user", "created_at", "reaction_count"]


class CommentNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["text"]
