import bcrypt

from models.model import Model
from models.session import Session
from models.location import Location


class User(Model):
    table = "users"

    def __init__(self, id: int, username: str, password_hash: bytes, email: str) -> None:
        super().__init__(id)
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

    def get_id(self):
        return self.id

    def check_pass(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode(), self.password_hash)

    def get_sessions(self) -> list[Session]:
        return [s for s in Session.get_all() if s.user_id == self.id]

    def get_locations(self) -> list[Location]:
        return [l for l in Location.get_all() if l.user_id == self.id]

    @classmethod
    def hash_password(cls: "User", password: str) -> bytes:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


    @classmethod
    def create(cls: "User", *args) -> "User":
        args = list(args)
        args[1] = cls.hash_password(args[1])

        return super().create(cls, args)