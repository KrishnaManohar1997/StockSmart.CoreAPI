import datetime

import jwt
from django.conf import settings

secret = settings.SMALLCASE_SECRET
# Smallcase Doc for JWT generation
# https://developers.gateway.smallcase.com/page/create-jwts-in-net
class SmallcaseJWTHelper:
    @staticmethod
    def get_smallcase_jwt(smallcase_auth_id=None):
        issue_at = datetime.datetime.utcnow()
        expire_at = issue_at + datetime.timedelta(days=1)
        if smallcase_auth_id in [None, ""]:
            return jwt.encode(
                {
                    "guest": True,
                    "exp": expire_at,
                    "iat": issue_at,
                },
                secret,
                algorithm="HS256",
            )
        return jwt.encode(
            {
                "smallcaseAuthId": smallcase_auth_id,
                "exp": expire_at,
                "iat": issue_at,
            },
            secret,
            algorithm="HS256",
        )

    @staticmethod
    def extract_smallcase_auth_id(user_logged_jwt_token: str):
        decoded_token_data = jwt.decode(
            user_logged_jwt_token, secret, algorithms=["HS256"]
        )
        if "smallcaseAuthId" not in decoded_token_data:
            return None
        return decoded_token_data.get("smallcaseAuthId")

    @staticmethod
    def get_stocksmart_logged_jwt_token():
        return SmallcaseJWTHelper.get_smallcase_jwt(
            settings.STOCKSMART_SMALLCASE_AUTH_ID
        )
