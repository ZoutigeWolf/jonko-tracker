from datetime import datetime
from typing import Union

from models.model import Model


class Session(Model):
    table = "sessions"

    def __init__(self, id: int, location_id: int, date_time: Union[str, datetime], user_id: int) -> None:
        super().__init__(id)
        self.location_id = location_id
        self.date_time = date_time if isinstance(date_time, datetime) else datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S.%f")
        self.user_id = user_id
