import os
import base64
from datetime import datetime

from database import database


class PasswordResetSession:
    def __init__(self, id: int, user_id: int, token: str, created_at: str | datetime) -> None:
        self.id = id
        self.user_id = user_id
        self.token = token
        self.created_at = created_at if isinstance(created_at, datetime) else datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S.%f")

    def delete(self) -> None:
        database.execute("DELETE FROM password_reset_sessions WHERE id = ?", (self.id,))
        database.commit()

    @staticmethod
    def generate_token() -> str:
        return base64.b64encode(os.urandom(64)).decode('utf-8').replace("+", "-").replace("?", "-")

    @staticmethod
    def create_session(user_id: int) -> "PasswordResetSession":
        user = PasswordResetSession(
            PasswordResetSession.get_next_id(),
            user_id,
            PasswordResetSession.generate_token(),
            datetime.now()
        )

        database.execute(
            "INSERT INTO password_reset_sessions (id, user_id, token, created_at) VALUES(?, ?, ?, ?)",
            tuple(user.__dict__.values())
        )
        database.commit()

        return user

    @staticmethod
    def get_all_sessions() -> list["PasswordResetSession"]:
        return [PasswordResetSession(*r) for r in database.execute("SELECT * FROM password_reset_sessions").fetchall()]

    @staticmethod
    def get_session_by_id(session_id: int) -> "PasswordResetSession":
        res = [s for s in PasswordResetSession.get_all_sessions() if s.id == session_id]

        return None if len(res) == 0 else res[0]

    @staticmethod
    def get_session_by_user_id(user_id: int) -> "PasswordResetSession":
        res = [s for s in PasswordResetSession.get_all_sessions() if s.user_id == user_id]

        return None if len(res) == 0 else res[0]

    @staticmethod
    def get_session_by_token(token: str) -> "PasswordResetSession":
        res = [s for s in PasswordResetSession.get_all_sessions() if s.token == token]

        return None if len(res) == 0 else res[0]

    @staticmethod
    def get_next_id() -> int:
        return max([s.id for s in PasswordResetSession.get_all_sessions()], default=0) + 1
