from django.core.exceptions import ValidationError
from rest_framework import status


class PermissionDeniedError(ValidationError):
    def __init__(self, message):
        raise ValidationError(message, code=status.HTTP_403_FORBIDDEN)
