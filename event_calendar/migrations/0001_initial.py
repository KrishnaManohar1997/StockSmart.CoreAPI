# Generated by Django 3.2.5 on 2021-11-03 12:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("stock", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="EventCalendar",
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
                    "event_type",
                    models.CharField(
                        choices=[
                            ("NSE Holiday", "Nse Holiday"),
                            ("Non Working Day", "Nse Non Working Day"),
                            ("NSE Ticker Result", "Nse Ticker Result"),
                            ("NSE Ticker Event", "Nse Ticker Event"),
                            ("NSE Ticker Announcement", "Nse Ticker Announcement"),
                        ],
                        db_index=True,
                        max_length=32,
                    ),
                ),
                ("published_at", models.DateTimeField()),
                ("description", models.TextField()),
                ("purpose", models.TextField()),
                ("attachment_url", models.URLField(blank=True, null=True)),
                ("event_data", models.JSONField(blank=True, default=dict, null=True)),
                (
                    "source_id",
                    models.CharField(blank=True, max_length=16, null=True, unique=True),
                ),
                (
                    "created_by_user",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="eventcalendar_created_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "symbol",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING, to="stock.stock"
                    ),
                ),
            ],
            options={
                "verbose_name": "Event_Calendar",
                "verbose_name_plural": "Event_Calendar",
                "db_table": "Event_Calendar",
                "unique_together": {("symbol", "event_type", "published_at")},
            },
        ),
    ]