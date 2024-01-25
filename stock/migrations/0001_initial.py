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
            name="Stock",
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
                ("symbol", models.CharField(db_index=True, max_length=32, unique=True)),
                ("name", models.CharField(db_index=True, max_length=128)),
                (
                    "last_news_fetched_at",
                    models.DateTimeField(blank=True, default=None, null=True),
                ),
                (
                    "latest_pub_news_date",
                    models.DateTimeField(blank=True, default=None, null=True),
                ),
                ("logo_url", models.URLField(blank=True, null=True)),
                (
                    "price_52_week_high",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "price_52_week_low",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                ("industry", models.CharField(blank=True, max_length=64, null=True)),
                (
                    "created_by_user",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="stock_created_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Stock",
                "verbose_name_plural": "Stocks",
                "db_table": "Stock",
            },
        ),
    ]
