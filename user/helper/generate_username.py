from django.conf import settings
from django.utils.crypto import get_random_string

from user.services import UserService

MAX_USERNAME_LENGTH = settings.USERNAME_MAX_LENGTH
from django.core.validators import validate_email


def sanitize_username(username):
    try:
        validate_email(username)
        username = username.split("@")[0]
    except Exception:
        pass
    # Preserves only -> [a-z][A-Z][0-9]
    username = "".join(_ for _ in username if (_.isalnum()))
    return username


def replace_available_username(social_user_name):
    social_user_name = sanitize_username(social_user_name)
    username_length = len(social_user_name)
    if username_length < 3:
        social_user_name = social_user_name + get_random_string(2)
    elif username_length > 12:
        social_user_name = social_user_name[:MAX_USERNAME_LENGTH]

    while not UserService().is_username_available(username=social_user_name):
        social_user_name = (
            f"{social_user_name[:MAX_USERNAME_LENGTH-2]}{get_random_string(2)}"
        )
    return social_user_name
