from django.core.management.base import BaseCommand
from user.models import User


class Command(BaseCommand):
    help = "Creates Users"

    def handle(self, *args, **options):
        User.objects.create_user(
            name="John Kransiki",
            email="john@mail.com",
            username="john12",
            is_superuser=True,
            is_staff=True,
            password="admin",
        )

        User.objects.create_user(
            name="manohar Admin",
            email="manohar@mail.com",
            username="manohar",
            is_superuser=True,
            is_staff=True,
            password="admin",
        )

        User.objects.create_user(
            name="aakash Kedu",
            email="aakash@mail.com",
            username="aakashkedu",
            is_superuser=True,
            is_staff=True,
            password="admin",
        )
        User.objects.create_user(
            name="rahul ganji",
            email="rahul@mail.com",
            username="rahulmaster",
            is_superuser=True,
            is_staff=True,
            password="admin",
        )
