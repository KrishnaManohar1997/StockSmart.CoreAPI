from rest_framework.permissions import IsAuthenticated

from common.base_view import BaseView
from user.permissions import IsBlockedByUser
from user.serializers import PublicUserSerializer
from user.services import UserService
from user.views.user_profile_view import UserProfileView


class PublicUserProfileView(BaseView):
    permission_classes = [IsAuthenticated, IsBlockedByUser]
    user_service = UserService()
    serializer = PublicUserSerializer

    def get(self, request, username: str):
        user = self.user_service.get_user_by_username(username)
        if not user:
            return self.resource_not_found_response("User", username)

        # If Requesting User is same as the target user
        # Render User Profile View
        if request.user.id == user.id:
            return UserProfileView().get(request)

        user_data = self.serializer(user, context={"request": request}).data
        return self.data_response(message="User details", data=user_data)
