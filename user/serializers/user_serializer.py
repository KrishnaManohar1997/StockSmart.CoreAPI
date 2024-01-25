import string
from datetime import datetime, timezone

from rest_framework import serializers

from common.helper.text_sanitizer import sanitize_text
from user.models import User
from user.services import UserService


class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "name",
            "profile_picture_url",
            "verified_professional_accounts",
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "date_joined",
            "name",
            "username",
            "email",
            "date_of_birth",
            "phone",
            "karma",
            "success_rate",
            "about",
            "profile_picture_url",
            "followers_count",
            "following_count",
            "verified_professional_accounts",
            "is_broker_connected",
            "is_import_holdings_authorized",
        ]


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    user_service = UserService()

    class Meta:
        model = User
        fields = [
            "name",
            "username",
            "about",
            "phone",
            "date_of_birth",
            "profile_picture_url",
        ]

    def validate_date_of_birth(self, dob):
        if datetime.now(timezone.utc).date() <= dob:
            raise serializers.ValidationError("Cannot be a future date")
        # if the DOB is unchanged
        return dob

    def validate_phone(self, phone):
        # if the phone number is unchanged
        if self.instance.phone == phone:
            return phone
        if not self.user_service.is_phone_valid(phone):
            raise serializers.ValidationError("Phone Number is not Valid")
        if not self.user_service.is_phone_available(phone):
            raise serializers.ValidationError("Phone number is not Available")
        return phone

    def validate_username(self, username):
        # if the username is unchanged
        if self.instance.username == username:
            return username
        if not self.user_service.is_username_valid(username):
            raise serializers.ValidationError("Username is not Valid")
        if not self.user_service.is_username_available(username):
            raise serializers.ValidationError("Username is not Available")
        return username

    def validate_name(self, name):
        for _ in name:
            if _ not in [*list(string.ascii_letters), " "]:
                raise serializers.ValidationError("cannot have invalid chars")
        return name

    def validate(self, data):
        SANITIZE_KEYS = ["about", "name"]
        for _ in SANITIZE_KEYS:
            _data = data.get(_)
            if _data:
                data[_] = sanitize_text(data[_], strip_data=True).strip()
        return data
