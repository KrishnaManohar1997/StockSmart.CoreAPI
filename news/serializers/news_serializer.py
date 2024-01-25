from news.models import News
from rest_framework.serializers import ModelSerializer


class NewsSerializer(ModelSerializer):
    class Meta:
        model = News
        fields = [
            "title",
            "description",
            "source_name",
            "url",
            "image_url",
            "published_at",
        ]
