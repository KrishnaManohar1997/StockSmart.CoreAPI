import django.utils.timezone as dj_datetime
from django.db.models.query import QuerySet

from user.models import User


class UserRepository:
    def get_user_by_id(self, user_id):
        return User.objects.get(pk=user_id)

    def is_username_available(self, username: str) -> bool:
        return not User.objects.filter(username__iexact=username).exists()

    def is_phone_available(self, phone: str) -> bool:
        return not User.objects.filter(phone=phone).exists()

    def get_users_by_matching_username(self, username: str) -> QuerySet[User]:
        return User.objects.filter(username__iexact=username)

    def get_user_by_username(self, username: str) -> User:
        """Gets the User by Username

        Args:
            username (str): Username (unique) to find a User

        Returns:
            User object matching with the username ignoring case
        Raises:
            User.DoesNotExist When matching User is not found
        """
        return User.objects.get(username__iexact=username)

    def ingest_smallcase_auth_id(self, user: User, smallcase_auth_id: str):
        user.smallcase_auth_id = smallcase_auth_id
        user.broker_connected_at = dj_datetime.now()
        user.save()
        return user

    def get_users_by_ids(self, user_list_ids: list):
        return User.objects.filter(id__in=user_list_ids)

    def get_users_by_username(self, username: str, blocked_user_ids: list):
        return User.objects.filter(username__icontains=username).exclude(
            id__in=blocked_user_ids
        )

    def get_non_blocked_users_by_ids(self, user_ids: list, blocked_user_ids: list):
        return self.get_users_by_ids(user_ids).exclude(id__in=blocked_user_ids)

    def get_user_created_posts(self, user):
        return user.post_created_by.all().order_by("-created_at")

    def get_user_by_smallcase_auth_id(self, smallcase_auth_id):
        return User.objects.get(smallcase_auth_id=smallcase_auth_id)

    def increment_user_karma(self, user, karma_score: int):
        user.karma += karma_score
        user.save()
        return user

    def get_all_users(self):
        return User.objects.all()

    def get_verified_user_ids(self):
        return User.objects.filter(
            verified_professional_accounts__isnull=False
        ).values_list("id", flat=True)
