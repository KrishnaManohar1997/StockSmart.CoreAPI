from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class User(AbstractUser):
    objects = UserManager()
    first_name = models.CharField(max_length=256, blank=False, null=False)
    last_name = models.CharField(max_length=256, blank=False, null=False)
    username = models.CharField(max_length=256, blank=True, null=True)
    phone = models.CharField(max_length=16, unique=True, blank=True, null=True)
    country_code = models.CharField(max_length=4, default="+91")
    email = models.EmailField(blank=False, null=False, unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name", "phone"]

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = "User"
        swappable = "AUTH_USER_MODEL"
