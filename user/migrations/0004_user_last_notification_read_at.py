# Generated by Django 3.2.5 on 2022-01-08 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0003_user_success_rate"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="last_notification_read_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
