from rest_framework import serializers
from common.helper.market_status import is_market_open_on_day
from common.helper.stocksmart_file_url_validation import is_stocksmart_file_url

from common.helper.text_sanitizer import sanitize_text
from post.models import Post


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "content",
            "media",
            "signal_type",
            "url",
            "created_by_user",
            "mentions",
            "source",
            "target_price",
            "signal_expire_at",
        ]

    def validate_signal_expire_at(self, signal_expire_at):
        if not signal_expire_at:
            return
        if not is_market_open_on_day(signal_expire_at):
            raise serializers.ValidationError(
                "Signal Expiry cannot be on a Market Closed day"
            )

        return signal_expire_at

    def validate_media(self, media):
        if not media:
            return
        if not is_stocksmart_file_url(media):
            raise serializers.ValidationError("Media URL is Invalid")
        return media

    def validate(self, data):
        data["content"] = sanitize_text(data["content"]).strip()
        return data
