# Generated by Django 3.2.5 on 2021-11-03 12:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import gm2m.fields
import post.helpers.post_mentions_json_schema
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("mentions", "0001_initial"),
        ("contenttypes", "0002_remove_content_type_name"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Post",
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
                    "signal_type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Bullish", "Bullish"),
                            ("Bearish", "Bearish"),
                            ("None", "Neutral"),
                        ],
                        default="None",
                        max_length=16,
                        null=True,
                    ),
                ),
                ("content", models.CharField(max_length=1024)),
                ("url", models.CharField(db_index=True, max_length=128, unique=True)),
                ("media", models.URLField(blank=True, null=True)),
                ("signal_expire_at", models.DateTimeField(blank=True, null=True)),
                ("reaction_count", models.PositiveIntegerField(default=0)),
                ("comment_count", models.PositiveIntegerField(default=0)),
                (
                    "mentions",
                    models.JSONField(
                        default=post.helpers.post_mentions_json_schema.get_post_mentions_schema
                    ),
                ),
                (
                    "created_by_user",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="post_created_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "ticker_mentions",
                    gm2m.fields.GM2MField(
                        "stock.Stock",
                        "smallcase.Smallcase",
                        through="mentions.PostTickerMention",
                        through_fields=["post", "ticker", "ticker_type", "ticker_id"],
                    ),
                ),
                (
                    "user_mentions",
                    models.ManyToManyField(
                        related_name="post_mentions",
                        through="mentions.PostUserMention",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Post",
                "verbose_name_plural": "Posts",
                "db_table": "Post",
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="Comment",
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
                ("text", models.CharField(max_length=512)),
                ("reaction_count", models.PositiveIntegerField(default=0)),
                ("object_id", models.UUIDField(db_index=True, editable=False)),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "created_by_user",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comment_created_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Comment",
                "verbose_name_plural": "Comments",
                "db_table": "Comment",
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="Reaction",
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
                    "reaction",
                    models.CharField(
                        choices=[
                            ("Like", "Like"),
                            ("RemoveReaction", "Remove Reaction"),
                        ],
                        default="Like",
                        max_length=16,
                    ),
                ),
                ("object_id", models.UUIDField(db_index=True, editable=False)),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "created_by_user",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reaction_created_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Reaction",
                "verbose_name_plural": "Reactions",
                "db_table": "Reaction",
                "managed": True,
                "unique_together": {("object_id", "id")},
            },
        ),
    ]
