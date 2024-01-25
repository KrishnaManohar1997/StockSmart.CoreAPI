from rest_framework.permissions import BasePermission

from user.models import UserFriendship
from user.services import UserFriendshipService, UserService


class IsBlockedByUser(BasePermission):
    """
    Checks if the Target User has blocked the requesting user
    """

    message = {"message": "User request denied"}

    def has_permission(self, request, view):
        target_user = None
        user_service = UserService()
        if "username" in view.kwargs:
            target_user = user_service.get_user_by_username(view.kwargs["username"])
        elif "social_user_id" in view.kwargs:
            social_user_id = view.kwargs["social_user_id"]
            # If requesting user and target user are same
            if social_user_id == str(request.user.id):
                return True
            target_user = user_service.get_user_by_id_or_none(social_user_id)

        if target_user:
            user_friendship = UserFriendshipService().get_user_friendship_or_none(
                str(target_user.id), str(request.user.id)
            )
            # If no friendship is present or friendship is not blocked
            # Then user can view/perform actions
            if (not user_friendship) or (
                user_friendship.friendship != UserFriendship.UserFriendshipType.BLOCKED
            ):
                return True
            return False
        return True
