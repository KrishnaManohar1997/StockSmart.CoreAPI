from common.base_view import BaseView
from user.services import UserService


class UsernameAvailabilityView(BaseView):
    user_service = UserService()

    def post(self, request, username: str):
        if not self.user_service.is_username_valid(username):
            return self.bad_request_response(message="Username is not valid")
        if not self.user_service.is_username_available(username):
            return self.bad_request_response(message="Username is not available")
        return self.success_response(message="Username is available")
