from datetime import datetime
from user.models import User


class UserRepository:
    def get_user(self, agent_id):
        return User.objects.get(pk=agent_id)

    def update_last_login(self, user_id):
        user = self.get_user(user_id)
        user.last_logged_in_at_utc = datetime.utcnow()
        user.save()
