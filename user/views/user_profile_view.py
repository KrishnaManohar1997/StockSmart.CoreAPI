from common.base_view import BaseView
from user.serializers import UserProfileSerializer, UserProfileUpdateSerializer


class UserProfileView(BaseView):
    serializer = UserProfileSerializer
    update_serializer = UserProfileUpdateSerializer

    def get(self, request):
        user_data = self.serializer(request.user).data
        return self.data_response(message="User details", data=user_data)

    def put(self, request):
        user_update_serializer = self.update_serializer(
            request.user, request.data, partial=True
        )
        if user_update_serializer.is_valid():
            user_update_serializer.save()
            return self.success_response("User details Updated")
        return self.serializer_error_response(
            "Failed updating user Details", user_update_serializer.errors
        )
