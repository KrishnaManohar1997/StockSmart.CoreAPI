from django.utils.translation import gettext_lazy as _
from rest_framework import HTTP_HEADER_ENCODING, exceptions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token

disabled_response = {"result": False, "message": "Invalid token"}


def get_authorization_header(request):
    """
    Return request's 'Authorization:' header, as a bytestring.

    Hide some test client ickyness where the header can be unicode.
    """
    auth = request.META.get("HTTP_AUTHORIZATION", b"")
    if isinstance(auth, str):
        # Work around django test client oddness
        auth = auth.encode(HTTP_HEADER_ENCODING)
    return auth


class StocksmartTokenAuthentication(TokenAuthentication):
    model = Token

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != self.keyword.lower().encode():
            msg = _("Authentication credentials were not provided.")
            raise exceptions.AuthenticationFailed({"result": False, "message": msg})
        if len(auth) == 1:
            msg = _("Invalid token header. No credentials provided.")
            raise exceptions.AuthenticationFailed({"result": False, "message": msg})
        elif len(auth) > 2:
            msg = _("Invalid token header. Token string should not contain spaces.")
            raise exceptions.AuthenticationFailed({"result": False, "message": msg})

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = _(
                "Invalid token header. Token string should not contain invalid characters."
            )
            raise exceptions.AuthenticationFailed({"result": False, "message": msg})

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        try:
            token = self.model.objects.select_related("user").get(key=key)
        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed(disabled_response)
        return (token.user, token)


class PublicAuthentication(TokenAuthentication):
    model = Token

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        # If token is not present still allow as Anonymous User
        if not auth:
            return
        return StocksmartTokenAuthentication().authenticate(request)
