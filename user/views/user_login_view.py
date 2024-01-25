from rest_framework.authtoken.views import ObtainAuthToken

from common.base_view import BaseView

from user.services import UserService


class UserLoginView(ObtainAuthToken, BaseView):
    authentication_classes = []
    user_service = UserService()

    def __preprocess_login_details(self, login_data: dict):
        if "email" in login_data:
            # Inputs email address in lower case
            email_address = login_data.pop("email")
            login_data["username"] = email_address.lower()
        return login_data

    def post(self, request):
        login_details = self.__preprocess_login_details(request.data)
        serializer = self.serializer_class(
            data=login_details, context={"request": request}
        )
        if not serializer.is_valid():
            return self.serializer_error_response(
                "Authentication failed ", serializer.errors
            )
        user_data = self.user_service.get_loggedin_user_details_with_token(
            serializer.validated_data["user"]
        )
        return self.data_response(message="User details", data=user_data)
