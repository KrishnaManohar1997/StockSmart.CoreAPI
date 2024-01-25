# Generated by Django 3.2.5 on 2021-11-03 12:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="PostTickerMention",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True, null=True)),
                ("is_deleted", models.BooleanField(default=False)),
                (
                    "watchlisted_market_price",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                ("ticker_id", models.UUIDField(db_index=True, editable=False)),
            ],
            options={
                "verbose_name": "Post_Ticker_Mention",
                "verbose_name_plural": "Post Ticker Mentions",
                "db_table": "Post_Ticker_Mention",
            },
        ),
        migrations.CreateModel(
            name="PostUserMention",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True, null=True)),
                ("is_deleted", models.BooleanField(default=False)),
                (
                    "created_by_user",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="postusermention_created_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "mentioned_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Post_User_Mention",
                "verbose_name_plural": "Post User Mentions",
                "db_table": "Post_User_Mention",
            },
        ),
    ]
