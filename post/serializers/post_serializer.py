from post.models import Post
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "id",
            "signal_type",
            "content",
            "signal_end_at",
            "created_at_utc",
            "modified_at_utc",
        ]
