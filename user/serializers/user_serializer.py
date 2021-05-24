from rest_framework import serializers
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "last_login",
            "date_joined",
            "first_name",
            "last_name",
            "username",
            "phone",
            "country_code",
            "email",
        ]
