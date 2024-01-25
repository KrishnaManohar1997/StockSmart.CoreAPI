from user.repositories.auth_token_repository import AuthTokenRepository


class AuthTokenService:
    auth_token_repo = AuthTokenRepository()

    def get_or_create_token(self, user_id):
        return self.auth_token_repo.get_or_create_token(user_id)

    def regenerate_token(self, user_id):
        return self.auth_token_repo.regenerate_token(user_id)

    def get_user_by_token(self, token):
        return self.auth_token_repo.get_user_by_token(token)
