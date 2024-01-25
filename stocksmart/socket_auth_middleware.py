from channels.db import database_sync_to_async
from urllib.parse import parse_qsl
from user.services import AuthTokenService


@database_sync_to_async
def get_token_user(token):

    token_obj = AuthTokenService().get_user_by_token(token)
    if not token_obj:
        return None
    return token_obj.user


class SocketTokenAuthMiddleware:
    """
    Custom middleware (insecure) that takes user IDs from the query string.
    """

    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app

    async def __call__(self, scope, receive, send):
        # Look up user from query string (you should also do things like
        # checking if it is a valid user ID, or if scope["user"] is already
        # populated).
        query_params = dict(parse_qsl(scope["query_string"].decode("utf-8")))
        # If Token or User is None
        # It will be rejected in the ws.connect
        token = query_params.get("token", None)
        scope["user"] = await get_token_user(token)
        return await self.app(scope, receive, send)
