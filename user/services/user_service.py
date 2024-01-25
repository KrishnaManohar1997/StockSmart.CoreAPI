from django.conf import settings
from django.contrib.auth.models import update_last_login

from common.constants import KarmaBonusIntent
from user.models import User
from user.repositories import UserRepository
from user.services.auth_token_service import AuthTokenService


class UserService:
    user_repository = UserRepository()
    auth_token_service = AuthTokenService()

    def get_user_by_id(self, user_id):
        return self.user_repository.get_user_by_id(user_id)

    def get_user_by_id_or_none(self, user_id):
        try:
            return self.get_user_by_id(user_id)
        except User.DoesNotExist:
            return None

    def get_loggedin_user_details_with_token(self, user: User) -> dict:
        """Generates user details with Token

        Args:
            user (User): Serialized user object

        Returns:
            dict: User details along with login Token
        """
        update_last_login(None, user)
        token, _ = self.auth_token_service.get_or_create_token(user_id=user.id)
        from user.serializers import UserProfileSerializer

        user_serializer = UserProfileSerializer(user)
        serialized_data = user_serializer.data
        serialized_data["token"] = token.key
        return serialized_data

    def is_phone_valid(self, phone: str) -> bool:
        for _ in phone:
            if not _.isdigit():
                return False
        if len(phone) != 10:
            return False
        return True

    def is_username_valid(self, username: str, min_length: int = 3) -> bool:
        if username in ["", None]:
            return False
        username_length = len(username)
        if (
            username_length > settings.USERNAME_MAX_LENGTH
            or username_length < min_length
        ):
            return False
        if not username[0].isalpha():
            return False
        for _ in username:
            if not _.isalnum():
                return False
        return True

    def is_username_available(self, username: str) -> bool:
        return self.user_repository.is_username_available(username)

    def is_phone_available(self, phone: str) -> bool:
        return self.user_repository.is_phone_available(phone)

    def get_user_by_username(self, username: str) -> User or None:
        try:
            return self.user_repository.get_user_by_username(username)
        except User.DoesNotExist:
            return None

    def ingest_smallcase_auth_id(self, user: User, smallcase_auth_id: str) -> User:
        if (
            user.smallcase_auth_id == smallcase_auth_id
            or user.smallcase_auth_id is not None
        ):
            return False, "An active broker is attached to your account"
        if self.get_user_by_smallcase_auth_id(smallcase_auth_id):
            return (
                False,
                "Your Broker Id is connected to a different account. Please try with a different broker",
            )
        user = self.assign_karma_bonus(user, KarmaBonusIntent.BROKER_CONNECT)
        user = self.user_repository.ingest_smallcase_auth_id(user, smallcase_auth_id)
        return True, user

    def get_users_by_ids(self, user_list_ids: list):
        return self.user_repository.get_users_by_ids(user_list_ids)

    def get_users_by_username(self, username: str, requesting_user_id: str):
        blocked_user_ids = self.__get_blocked_by_user_ids(requesting_user_id)
        return self.user_repository.get_users_by_username(username, blocked_user_ids)

    def get_non_blocked_users_by_ids(self, user_ids: list, requesting_user_id: str):
        blocked_user_ids = self.__get_blocked_by_user_ids(requesting_user_id)
        return self.user_repository.get_non_blocked_users_by_ids(
            user_ids, blocked_user_ids
        )

    def __get_blocked_by_user_ids(self, user_id):
        from user.services.user_friendship_service import UserFriendshipService

        return UserFriendshipService().get_blocked_by_user_ids(user_id)

    def get_blocked_by_user_ids(self, user_id):
        return self.__get_blocked_by_user_ids(user_id)

    def get_user_created_posts(self, user):
        return self.user_repository.get_user_created_posts(user)

    def get_user_by_smallcase_auth_id(self, smallcase_auth_id):
        try:
            return self.user_repository.get_user_by_smallcase_auth_id(smallcase_auth_id)
        except User.DoesNotExist:
            return None

    def assign_karma_bonus(self, user, karma_bonus_intent: KarmaBonusIntent) -> User:
        return self.increment_user_karma(user, karma_bonus_intent.value)

    def increment_user_karma(self, user, karma_score: int) -> User:
        return self.user_repository.increment_user_karma(user, karma_score)

    def get_all_users(self):
        return self.user_repository.get_all_users()

    def get_verified_user_ids(self):
        return self.user_repository.get_verified_user_ids()

    def get_user_rewards(self, user):
        return user.leaderboard_set.all()
