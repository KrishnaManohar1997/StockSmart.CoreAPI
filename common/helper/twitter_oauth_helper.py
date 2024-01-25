import requests
from django.conf import settings
from twython import Twython
from urllib import parse

twitter = Twython(settings.SOCIAL_AUTH_TWITTER_KEY, settings.SOCIAL_AUTH_TWITTER_SECRET)


def get_twitter_client_token() -> dict:
    """Generates the Oauth Token and Oauth Token secret
    for Client to make authorize API call to twitter

    Returns:
        dict: Dictionary of Oauth Token and Oauth Token Secret
    """
    auth = twitter.get_authentication_tokens(
        callback_url=settings.STOCKSMART_WEB_CLIENT
    )
    OAUTH_TOKEN = auth["oauth_token"]
    OAUTH_TOKEN_SECRET = auth["oauth_token_secret"]
    # NOTE: Use the following Key if FE is facing issues
    # auth["oauth_callback_confirmed"]
    return {"oauth_token": OAUTH_TOKEN, "oauth_token_secret": OAUTH_TOKEN_SECRET}


def get_social_auth_twitter_token(request_data: dict) -> str or None:
    token_dict = request_data.get("token")
    oauth_dict = generate_bearer_oauth_token(
        token_dict["oauth_token"], token_dict["oauth_verifier"]
    )
    if oauth_dict is not None:
        return parse.urlencode(oauth_dict)


def generate_bearer_oauth_token(oauth_token: str, oauth_verifier: str) -> dict or None:
    query_params = {"oauth_token": oauth_token, "oauth_verifier": oauth_verifier}
    bearer_token_response = requests.post(
        f"https://api.twitter.com/oauth/access_token", params=query_params
    )
    if bearer_token_response.status_code == 200:
        bearer_token_content = bearer_token_response.content.decode("utf-8")
        oauth_dict = dict(parse.parse_qsl(bearer_token_content))
        return {
            "oauth_token": oauth_dict["oauth_token"],
            "oauth_token_secret": oauth_dict["oauth_token_secret"],
        }
