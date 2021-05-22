# Generated by Django 3.2.3 on 2021-05-22 12:14

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

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
                ("name", models.CharField(db_index=True, max_length=128, unique=True)),
                ("symbol", models.CharField(db_index=True, max_length=16, unique=True)),
                ("last_traded_at_price", models.CharField(max_length=64)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("SIMPLE", "Simple"),
                            ("FINANCIAL", "Financial"),
                            ("UTILITY", "Utility"),
                            ("CONSUMER_DISCRETIONARY", "ConsumerDiscretionary"),
                            ("ENERGY", "Energy"),
                            ("HEALTHCARE", "Healthcare"),
                            ("INDUSTRIAL", "Industrial"),
                            ("TECHNOLOGY", "Technology"),
                            ("TELECOM", "Telecom"),
                            ("MATERIAL", "Material"),
                            ("REAL_ESTATE", "RealEstate"),
                        ],
                        default="Financial",
                        max_length=24,
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("EQUITY", "Equity"),
                            ("DEBT", "Debt"),
                            ("DERIVATIVES", "Derivatives"),
                        ],
                        default="Equity",
                        max_length=16,
                    ),
                ),
            ],
            options={
                "verbose_name": "Stock",
                "verbose_name_plural": "Stocks",
                "db_table": "Stock",
                "managed": True,
            },
        ),
    ]