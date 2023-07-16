import bcrypt

from database import database


class User:
    def __init__(self, id: int, username: str, password_hash: bytes, email: str) -> None:
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.email = email

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

    def update(self, username: str = None, password: str = None, email: str = None) -> None:
        if username is not None:
            self.username = username

        if password is not None:
            self.password_hash = User.hash_password(password)

        if email is not None:
            self.email = email

        database.execute(
            "UPDATE users SET username = ?, password_hash = ?, email = ? WHERE id = ?",
            (self.username, self.password_hash, self.email, self.id)
        )
        database.commit()

    @staticmethod
    def hash_password(password: str) -> bytes:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    @staticmethod
    def create_user(username: str, password: str, email: str) -> "User":
        user = User(User.get_next_id(), username, User.hash_password(password), email)
        database.execute(
            "INSERT INTO users (id, username, password_hash, email) VALUES(?, ?, ?, ?)",
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
    def get_user_by_email(email: str) -> "User":
        res = [u for u in User.get_all_users() if u.email == email]

        return None if len(res) == 0 else res[0]

    @staticmethod
    def get_next_id() -> int:
        return max([u.id for u in User.get_all_users()], default=0) + 1


from models.session import Session
from models.location import Location
