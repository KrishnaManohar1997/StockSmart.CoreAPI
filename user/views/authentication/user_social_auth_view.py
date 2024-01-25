import structlog
from drf_social_oauth2.views import ConvertTokenView
from oauth2_provider.models import AccessToken

from common.base_view import BaseView
from common.helper.twitter_oauth_helper import get_social_auth_twitter_token
from user.services.user_service import UserService

logger = structlog.getLogger("django.server")


class UserSocialAuthView(ConvertTokenView, BaseView):
    authentication_classes = []
    user_service = UserService()

    def post(self, request, *args, **kwargs):
        backend = ""
        try:
            backend = request.data.get("backend", "")
            if backend.lower() == "twitter":
                twitter_auth_token = get_social_auth_twitter_token(request.data)
                if twitter_auth_token:
                    request.data["token"] = twitter_auth_token

            # Converts Access Token from Oauth to Bearer Token
            response = super(UserSocialAuthView, self).post(request, *args, **kwargs)
            if "access_token" not in response.data:
                if "access_denied" == response.data["error"]:
                    return self.unauthorized_response(
                        message=f"{response.data['error_description']}"
                    )
                return self.unauthorized_response(
                    message=f"Authentication Failed {backend}, Please try again later"
                )
            token = AccessToken.objects.get(token=response.data["access_token"])
            # Retrieves User from Access Token
            user = token.user
            user_data = self.user_service.get_loggedin_user_details_with_token(user)
            return self.data_response(message="Successfully logged in", data=user_data)
        except Exception as error:
            logger.error(f"Error User Signup with Backend {backend}", error=error)
        return self.bad_request_response("Please try again Logging in")
