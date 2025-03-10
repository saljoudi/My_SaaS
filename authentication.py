from flask_login import UserMixin
from database import get_user

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    @staticmethod
    def get(user_id):
        user = get_user(user_id)
        if user:
            return User(id=user['id'], username=user['username'], password=user['password'])
        return None
