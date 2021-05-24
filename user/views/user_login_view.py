from user.services.auth_token_service import AuthTokenService
from user.services.user_service import UserService
from user.models.user_model import User
from user.serializers.user_serializer import UserSerializer
from common.base_view import BaseView
from rest_framework.authtoken.views import ObtainAuthToken


class UserLoginView(ObtainAuthToken, BaseView):
    user_service = UserService()
    auth_token_service = AuthTokenService()

    def __preprocess_login_details(self, login_data: dict):
        if "email" in login_data:
            # Inputs email address in lower case
            email_address = login_data.pop("email")
            login_data["username"] = email_address.lower()
        return login_data

    def __get_loggedin_user_details(self, user: User) -> dict:
        """Generates user details with Token

        Args:
            user (User): Serialized user object

        Returns:
            dict: User details along with login Token
        """
        self.user_service.update_last_login(user.id)
        token, created = self.auth_token_service.get_or_create_token(user_id=user.id)
        user_serializer = UserSerializer(user)
        serialized_data = user_serializer.data
        serialized_data["token"] = token.key
        return serialized_data

    def post(self, request):
        login_details = self.__preprocess_login_details(request.data)
        serializer = self.serializer_class(
            data=login_details, context={"request": request}
        )
        if not serializer.is_valid():
            return self.serializer_error_response(
                "Authentication failed ", serializer.errors
            )
        user_data = self.__get_loggedin_user_details(serializer.validated_data["user"])
        return self.data_response(message="User details", data=user_data)
