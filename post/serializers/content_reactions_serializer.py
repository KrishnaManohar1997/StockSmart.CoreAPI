from rest_framework import serializers

from post.models import Reaction

from user.serializers import CommentUserSerializer


class ContentReactionsSerializer(serializers.ModelSerializer):
    created_by_user = CommentUserSerializer()

    class Meta:
        model = Reaction
        fields = ["created_by_user"]
