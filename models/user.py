from database import database
import bcrypt


class User:
    def __init__(self, id: int, username: str, password_hash: bytes) -> None:
        self.id = id
        self.username = username
        self.password_hash = password_hash

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return self.is_active

    @property
    def is_anonymous(self):
        return False

    def check_pass(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode(), self.password_hash)

    def get_id(self):
        return self.id

    def get_sessions(self) -> list["Session"]:
        return [s for s in Session.get_all_sessions() if s.user_id == self.id]

    def get_locations(self) -> list["Location"]:
        return [l for l in Location.get_all_locations() if l.user_id == self.id]

    @staticmethod
    def create_user(username: str, password: str) -> "User":
        user = User(User.get_next_id(), username, bcrypt.hashpw(password.encode(), bcrypt.gensalt()))
        database.execute(
            "INSERT INTO users (id, username, password_hash) VALUES(?, ?, ?)",
            tuple(user.__dict__.values())
        )
        database.commit()

        return user

    @staticmethod
    def get_all_users() -> list["User"]:
        return [User(*r) for r in database.execute("SELECT * FROM users").fetchall()]

    @staticmethod
    def get_user_by_id(user_id: int) -> "User":
        res = [u for u in User.get_all_users() if u.id == user_id]

        return None if len(res) == 0 else res[0]

    @staticmethod
    def get_user_by_username(username: str) -> "User":
        res = [u for u in User.get_all_users() if u.username == username]

        return None if len(res) == 0 else res[0]

    @staticmethod
    def get_next_id() -> int:
        return max([u.id for u in User.get_all_users()], default=0) + 1


from session import Session
from location import Location