from models.user import User
from models.session import Session
from models.location import Location


class Statistics:
    def __init__(self, user_id: int):
        self.user_id = user_id

    @property
    def user(self):
        return User.get_user_by_id(self.user_id)


