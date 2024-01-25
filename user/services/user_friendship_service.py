from typing import Tuple

from django.core.exceptions import ValidationError

from notification.services import NotificationService
from stocksmart.celery import app
from user.models import User, UserFriendship
from user.repositories import UserFriendshipRepository
from user.services import UserService


class UserFriendshipService:
    user_friendship_repo = UserFriendshipRepository()
    user_service = UserService()

    def perform_friendship_action(
        self, action: str, relating_user: User, related_user_id: str
    ) -> Tuple[bool, str]:
        related_user = self.user_service.get_user_by_id(related_user_id)
        if action == UserFriendship.UserFriendshipType.FOLLOW:
            return self.follow_user(relating_user, related_user)
        elif action == UserFriendship.UserFriendshipType.NO_FRIENDSHIP:
            return self.unfollow_user(relating_user, related_user)
        elif action == UserFriendship.UserFriendshipType.BLOCKED:
            return self.block_user(relating_user, related_user)
        elif action == UserFriendship.UserFriendshipType.UNBLOCK:
            return self.unblock_user(relating_user, related_user)
        return False, "Action not available"

    def get_user_friendship_or_none(self, relating_user_id: str, related_user_id: str):
        return self.user_friendship_repo.get_user_friendship_or_none(
            relating_user_id, related_user_id
        )

    def is_requesting_user_blocked_by_user(
        self, requesting_user_id: str, target_user_id: str, raise_error=False
    ) -> bool:
        """Checks if the requesting user is blocked by target user

        Args:
            requesting_user_id (str): User trying to access content created by any other user
            target_user_id (str): User Id owner of any content
            raise_error (bool, optional): Raises Validation Error if blocked by the user. Defaults to False.

        Returns:
            bool: True if blocked by the target user
        """
        # If target and requesting user are same allow
        if requesting_user_id == target_user_id:
            return False

        is_blocked = self.user_friendship_repo.is_requesting_user_blocked_by_user(
            requesting_user_id, target_user_id
        )
        if not raise_error or (raise_error and not is_blocked):
            return is_blocked
        raise ValidationError("Action cannot be performed", code=403)

    def follow_user(self, relating_user: User, related_user: User) -> Tuple[bool, str]:
        # Get Requesting User's friendship with related user
        reverse_user_friendship = self.get_user_friendship_or_none(
            related_user.id, relating_user.id
        )
        if (
            reverse_user_friendship
            and reverse_user_friendship.friendship
            == UserFriendship.UserFriendshipType.BLOCKED
        ):
            return False, "You cannot perform this action"

        user_friendship = self.get_user_friendship_or_none(
            relating_user.id, related_user.id
        )
        # Create a Friendship if not exists and increase the respective
        # Follower and following count
        if not user_friendship:
            self.user_friendship_repo.follow_user(relating_user, related_user)

        # Even if the friendship exists as following already, we return success
        elif user_friendship.friendship == UserFriendship.UserFriendshipType.FOLLOW:
            return True, "User follow success"

        # If the User is blocked, then we raise an error
        elif user_friendship.friendship == UserFriendship.UserFriendshipType.BLOCKED:
            return False, "You should unblock the user first to perform the action"
        # If the User is Not Related, then we Update the status and increment the
        # Follower and Following Count
        elif (
            user_friendship.friendship
            == UserFriendship.UserFriendshipType.NO_FRIENDSHIP
        ):
            self.user_friendship_repo.update_friendship_as_follow(
                user_friendship, relating_user, related_user
            )
        # When new Follow Relation is created
        followed_by_user_id = str(relating_user.id)
        notify_user_id = str(related_user.id)
        NotificationService.user_follow_notification.apply_async(
            kwargs={
                "notify_user_id": notify_user_id,
                "followed_by_user_id": followed_by_user_id,
            },
            countdown=5,
        )
        return True, "User follow successful"

    def unfollow_user(
        self, relating_user: User, related_user: User
    ) -> Tuple[bool, str]:
        user_friendship = self.get_user_friendship_or_none(
            relating_user.id, related_user.id
        )
        # If there is no Friendship between the Users or
        # If the User has NO_FRIENDSHIP as friendship status
        # No changes are needed
        if (
            (not user_friendship)
            or user_friendship.friendship
            == UserFriendship.UserFriendshipType.NO_FRIENDSHIP
        ):
            return False, "You do not follow this user"
        # When the User already follow the requesting User, we change status back to no friendship
        # and decrease the Follower and Following count respectively
        if user_friendship.friendship == UserFriendship.UserFriendshipType.FOLLOW:
            self.user_friendship_repo.unfollow_user(relating_user, related_user)
        # Even if the User is already in Blocked State we send User unfollow successful
        # As no changes are needed
        return True, "User unfollow successful"

    def block_user(self, relating_user: User, related_user: User) -> Tuple[bool, str]:
        # Get Requesting User's friendship with related user
        reverse_user_friendship = self.get_user_friendship_or_none(
            related_user.id, relating_user.id
        )
        if (
            reverse_user_friendship
            and reverse_user_friendship.friendship
            == UserFriendship.UserFriendshipType.FOLLOW
        ):
            # Update the target user's friendship to No Friendship
            self.user_friendship_repo.unfollow_user(related_user, relating_user)

        user_friendship = self.get_user_friendship_or_none(
            relating_user.id, related_user.id
        )
        # If no friendship existed before
        # Scenario when someone blocks a Profile with no past friendship
        if not user_friendship:
            self.user_friendship_repo.create_blocked_friendship(
                relating_user, related_user
            )
        # Scenario where User already follows the person
        elif user_friendship.friendship == UserFriendship.UserFriendshipType.FOLLOW:
            # Change friendship status to Blocked and Update the Followers and following count
            self.user_friendship_repo.block_following_user(
                user_friendship, relating_user, related_user
            )

        # When friendship exists but not related
        elif (
            user_friendship.friendship
            == UserFriendship.UserFriendshipType.NO_FRIENDSHIP
        ):
            self.user_friendship_repo.block_nofriendship_user(user_friendship)
        # When already blocked automatically returns User Blocked successfully
        return True, "User blocked successfully"

    def unblock_user(self, relating_user: User, related_user: User) -> Tuple[bool, str]:
        user_friendship = self.get_user_friendship_or_none(
            relating_user.id, related_user.id
        )
        # If a friendship existed before and if it is blocked
        # Then unblock the User to No Friendship status
        if (
            user_friendship
            and user_friendship.friendship == UserFriendship.UserFriendshipType.BLOCKED
        ):
            # Change friendship status to unblocked
            self.user_friendship_repo.unblock_user(user_friendship)
        return True, "User unblocked successfully"

    def get_user_followers_list(self, user_id: str):
        return self.user_friendship_repo.get_user_followers_list(user_id)

    def get_user_following_list(self, user_id: str):
        return self.user_friendship_repo.get_user_following_list(user_id)

    def get_friendship_status(self, relating_user, user_ids: list):
        return self.user_friendship_repo.get_friendship_status(relating_user, user_ids)

    def get_friendship_status_list(self, relating_user, user_ids: list):
        friendship_status = self.get_friendship_status(relating_user, user_ids)
        friendship_data = dict.fromkeys(user_ids, None)
        for friend_id, friendship in friendship_status:
            friendship_data[str(friend_id)] = friendship
        return {
            "blocked_by_user_ids": self.get_blocked_by_user_ids(relating_user.id),
            "friendship_status": friendship_data,
        }

    def get_blocked_by_user_ids(self, user_id):
        return UserFriendship.objects.filter(
            related_user_id=user_id,
            friendship=UserFriendship.UserFriendshipType.BLOCKED,
        ).values_list("relating_user_id", flat=True)


@app.task()
def create_auto_follow_relation(new_user_id, ss_user_id):
    user = UserService().get_user_by_id(ss_user_id)
    UserFriendshipService().perform_friendship_action(
        UserFriendship.UserFriendshipType.FOLLOW, user, new_user_id
    )
