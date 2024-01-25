from common.base_view import PublicBaseView
from common.helper.twitter_oauth_helper import get_twitter_client_token


class TwitterClientOauthTokenView(PublicBaseView):
    def post(self, request):
        try:
            return self.data_response(
                message="Client Auth token details", data=get_twitter_client_token()
            )
        except Exception:
            return self.unauthorized_response(
                message="Client token cannot be generated"
            )
