from rest_framework.permissions import BasePermission


class IsUserFriendshipActionValid(BasePermission):
    """
    Doesn't allow User to follow/unfollow/block/unblock himself
    """

    message = {"message": "User request denied"}

    def has_permission(self, request, view):
        # If User Id is same as the requested user Id
        # Permission is denied for User Follow Action
        return str(request.user.id) != view.kwargs["social_user_id"]
