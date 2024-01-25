import os
import glob
import shutil
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Resets the database"

    def handle(self, *args, **options):
        base = str(settings.BASE_DIR)
        migrations = glob.glob(os.path.join(base, "*", "migrations"))

        for migration in migrations:
            shutil.rmtree(migration)

        apps = [migration.split("\\")[-2] for migration in migrations]
        for app in apps:
            os.system("python manage.py makemigrations %s" % app)
        os.system("python manage.py migrate")
