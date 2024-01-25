from rest_framework import serializers

from user.models import UserHolding


class UserHoldingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserHolding
        fields = ["holdings", "last_update", "broker_name"]
