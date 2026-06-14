from database.user_model import user_exists, update_last_seen, create_user

class UserManager:
    @staticmethod
    def resolve_user(user_id=None):
        if user_id is None or not user_exists(user_id):
            user_id = create_user()
        else:
            update_last_seen(user_id)
        return user_id