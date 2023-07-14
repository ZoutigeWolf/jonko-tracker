from datetime import datetime
from database import database


class Session:
    def __init__(self, id: int, location_id: int, date_time: datetime, user_id: int) -> None:
        self.id = id
        self.location_id = location_id
        self.date_time = date_time
        self.user_id = user_id

    @staticmethod
    def create_session(location_id: int, date_time: datetime, user_id: int) -> "Session":
        session = Session(Session.get_next_id(), location_id, date_time, user_id)
        database.execute(
            "INSERT INTO sessions (id, location_id, datetime, user_id) VALUES(?, ?, ?, ?)",
            tuple(session.__dict__.values())
        )
        database.commit()

        return session

    @staticmethod
    def get_all_sessions() -> list["Session"]:
        return [Session(*r) for r in database.execute("SELECT * FROM sessions").fetchall()]

    @staticmethod
    def get_session_by_id(session_id: int) -> "Session":
        res = [s for s in Session.get_all_sessions() if s.id == session_id]

        return None if len(res) == 0 else res[0]

    @staticmethod
    def get_next_id() -> int:
        return max([s.id for s in Session.get_all_sessions()], default=0) + 1


from location import Location