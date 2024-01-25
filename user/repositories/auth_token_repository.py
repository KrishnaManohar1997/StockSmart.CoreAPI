from rest_framework.authtoken.models import Token


class AuthTokenRepository:
    def get_or_create_token(self, user_id):
        return Token.objects.get_or_create(user_id=user_id)

    # Always returns one record at max as User_id has unique constraint
    def get_token_by_user_id(self, user_id):
        return Token.objects.filter(user_id=user_id)

    # Generates a random crypto token key
    def generate_token_key(self):
        return Token().generate_key()

    # Generates new Auth token for the User
    def regenerate_token(self, user_id):
        self.get_token_by_user_id(user_id=user_id).update(key=self.generate_token_key())

    def get_user_by_token(self, token):
        try:
            return Token.objects.get(key=token)
        except Token.DoesNotExist:
            return None
