# Generated by Django 3.2.5 on 2021-11-03 12:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("post", "0001_initial"),
        ("mentions", "0001_initial"),
        ("contenttypes", "0002_remove_content_type_name"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="postusermention",
            name="post",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING, to="post.post"
            ),
        ),
        migrations.AddField(
            model_name="posttickermention",
            name="created_by_user",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="posttickermention_created_by",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="posttickermention",
            name="post",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING, to="post.post"
            ),
        ),
        migrations.AddField(
            model_name="posttickermention",
            name="ticker_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="contenttypes.contenttype",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="posttickermention",
            unique_together={("post", "ticker_id")},
        ),
    ]