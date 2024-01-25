from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from common.models import BaseModel, SignupMethod
from report.models import Report


class User(AbstractUser, BaseModel):
    objects = UserManager()

    name = models.CharField(max_length=64, blank=False, null=False)
    email = models.EmailField(blank=False, null=False, unique=True, db_index=True)
    is_email_verified = models.BooleanField(default=False, blank=False, null=False)
    username = models.CharField(
        max_length=12, blank=True, null=True, unique=True, db_index=True
    )
    first_name = models.CharField(max_length=32, blank=True, null=True)
    last_name = models.CharField(max_length=32, blank=True, null=True)
    smallcase_auth_id = models.CharField(
        max_length=64, blank=True, null=True, unique=True
    )
    broker_connected_at = models.DateTimeField(null=True, blank=True)

    signup_method = models.CharField(
        max_length=16,
        choices=SignupMethod.choices,
        null=False,
        blank=False,
        default=SignupMethod.SIMPLE,
    )
    phone = models.CharField(max_length=16, blank=True, null=True, unique=True)
    country_code = models.CharField(max_length=4, null=True, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    karma = models.PositiveIntegerField(blank=True, default=0)
    about = models.CharField(max_length=512, blank=True, null=True)
    profile_picture_url = models.URLField(max_length=128, blank=True, null=True)
    verified_professional_accounts = models.JSONField(null=True, blank=True)
    profile_progress_score = models.PositiveIntegerField(default=0)
    user_friendships = models.ManyToManyField(
        "user.User",
        related_name="user_relations",
        through="user.UserFriendship",
        through_fields=(
            "relating_user",
            "related_user",
        ),
    )
    following_count = models.PositiveIntegerField(default=0)
    followers_count = models.PositiveIntegerField(default=0)
    success_rate = models.PositiveIntegerField(null=False, blank=False, default=0)
    last_notification_read_at = models.DateTimeField(blank=True, null=True)

    # Generic Relation for Reports on User
    reports = GenericRelation(Report)

    # NOTE: Default Joined Timestamp stored at `date_joined` field and
    # `last_login` is the default timestamp for the last user logged in datetime

    # Removing unnecessary Default User fields
    groups = None
    user_permissions = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "name"]

    def __str__(self):
        return self.email

    def is_broker_connected(self):
        return bool(self.smallcase_auth_id)

    def is_import_holdings_authorized(self):
        try:
            return bool(self.userholding)
        except ObjectDoesNotExist:
            return False

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = "User"
        swappable = "AUTH_USER_MODEL"
