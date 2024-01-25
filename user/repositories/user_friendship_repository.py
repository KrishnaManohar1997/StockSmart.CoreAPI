from user.models import User, UserFriendship
from django.db.models import F


class UserFriendshipRepository:
    def is_already_following(self, relating_user_id: str, related_user_id: str) -> bool:
        return UserFriendship.objects.filter(
            relating_user_id=relating_user_id,
            related_user_id=related_user_id,
            friendship=UserFriendship.UserFriendshipType.FOLLOW,
        ).exists()

    def get_user_friendship_or_none(
        self, relating_user_id: str, related_user_id: str
    ) -> bool or None:
        try:
            return UserFriendship.objects.get(
                relating_user_id=relating_user_id, related_user_id=related_user_id
            )
        except UserFriendship.DoesNotExist:
            return None

    def update_user_friendship_followers_count(
        self, relating_user: User, related_user: User, is_follow: bool
    ):
        if is_follow:
            relating_user.following_count = F("following_count") + 1
            related_user.followers_count = F("followers_count") + 1
        else:
            relating_user.following_count = F("following_count") - 1
            related_user.followers_count = F("followers_count") - 1

        relating_user.save(update_fields=["following_count"])
        related_user.save(update_fields=["followers_count"])

    def update_friendship_as_follow(self, user_friendship, relating_user, related_user):
        user_friendship.friendship = UserFriendship.UserFriendshipType.FOLLOW
        self.update_user_friendship_followers_count(
            relating_user, related_user, is_follow=True
        )
        user_friendship.save()

        return user_friendship

    def follow_user(self, relating_user: User, related_user: User):
        UserFriendship.objects.create(
            relating_user_id=relating_user.id,
            related_user_id=related_user.id,
            friendship=UserFriendship.UserFriendshipType.FOLLOW,
        )
        self.update_user_friendship_followers_count(
            relating_user, related_user, is_follow=True
        )

    def unfollow_user(self, relating_user: User, related_user: User):
        UserFriendship.objects.filter(
            relating_user_id=relating_user.id, related_user_id=related_user.id
        ).update(friendship=UserFriendship.UserFriendshipType.NO_FRIENDSHIP)
        self.update_user_friendship_followers_count(
            relating_user, related_user, is_follow=False
        )

    def update_friendship_as_blocked(self, user_friendship):
        user_friendship.friendship = UserFriendship.UserFriendshipType.BLOCKED
        user_friendship.save()
        return user_friendship

    def block_following_user(
        self, user_friendship, relating_user: User, related_user: User
    ):
        self.update_friendship_as_blocked(user_friendship)
        self.update_user_friendship_followers_count(
            relating_user, related_user, is_follow=False
        )

    def unblock_user(self, user_friendship):
        user_friendship.friendship = UserFriendship.UserFriendshipType.NO_FRIENDSHIP
        user_friendship.save()
        return user_friendship

    def block_nofriendship_user(self, user_friendship):
        self.update_friendship_as_blocked(user_friendship)

    def create_blocked_friendship(self, relating_user: User, related_user: User):
        return UserFriendship.objects.create(
            relating_user_id=relating_user.id,
            related_user_id=related_user.id,
            friendship=UserFriendship.UserFriendshipType.BLOCKED,
        )

    def get_user_followers_list(self, user_id: str):
        return UserFriendship.objects.filter(
            related_user_id=user_id, friendship=UserFriendship.UserFriendshipType.FOLLOW
        ).prefetch_related("relating_user")

    def get_user_following_list(self, user_id: str):
        return UserFriendship.objects.filter(
            relating_user_id=user_id,
            friendship=UserFriendship.UserFriendshipType.FOLLOW,
        ).prefetch_related("related_user")

    def get_friendship_status(self, relating_user, user_ids: list):
        return list(
            UserFriendship.objects.filter(
                relating_user=relating_user, related_user_id__in=user_ids
            ).values_list("related_user_id", "friendship")
        )

    def is_requesting_user_blocked_by_user(
        self, requesting_user_id: str, target_user_id: str
    ) -> bool:
        return UserFriendship.objects.filter(
            related_user_id=requesting_user_id,
            relating_user_id=target_user_id,
            friendship=UserFriendship.UserFriendshipType.BLOCKED,
        ).exists()
