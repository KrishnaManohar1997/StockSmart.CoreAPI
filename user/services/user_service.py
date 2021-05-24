from user.repositories.user_repository import UserRepository


class UserService:
    user_repository = UserRepository()

    def get_user(self, agent_id):
        return self.user_repository.get_user(agent_id)

    def update_last_login(self, user_id):
        self.user_repository.update_last_login(user_id)
