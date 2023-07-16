import os
import base64
from datetime import datetime
from typing import Union

from models.model import Model


class PasswordResetSession(Model):
    table = "password_reset_sessions"

    def __init__(self, id: int, user_id: int, token: str, created_at: Union[str, datetime]) -> None:
        super().__init__(id)
        self.user_id = user_id
        self.token = token
        self.created_at = created_at if isinstance(created_at, datetime) else datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S.%f")

    @classmethod
    def generate_token(cls: "PasswordResetSession") -> str:
        return base64.b64encode(os.urandom(64)).decode('utf-8').replace("+", "-").replace("?", "-")

    @classmethod
    def create(cls: "PasswordResetSession", *args) -> "PasswordResetSession":
        args = list(args)
        args.append(cls.generate_token())
        args.append(datetime.now())

        return super().create(args)
