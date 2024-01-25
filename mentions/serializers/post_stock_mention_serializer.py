from rest_framework import serializers

from mentions.models import PostTickerMention
from post.serializers import PostFeedSerializer


class PostStockMentionSerializer(serializers.ModelSerializer):
    post = PostFeedSerializer()

    class Meta:
        model = PostTickerMention
        fields = ["post"]
