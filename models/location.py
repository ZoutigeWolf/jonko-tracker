from datetime import datetime
from database import database


class Location:
    def __init__(self, id: int, name: str, latitude: float, longitude: float, user_id: int) -> None:
        self.id = id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.user_id = user_id

    def update(self, name: str, latitude: float, longitude: float) -> None:
        if name is not None:
            self.name = name

        if latitude is not None:
            self.latitude = latitude

        if longitude is not None:
            self.longitude = longitude

        database.execute(
            "UPDATE locations SET name = ?, latitude = ?, longitude = ? WHERE id = ?",
            (name, latitude, longitude, self.id)
        )
        database.commit()

    def delete(self) -> None:
        database.execute("DELETE FROM locations WHERE id = ?", (self.id,))
        database.commit()

    @staticmethod
    def create_location(name: str, latitude: float, longitude: float, user_id: int) -> "Location":
        location = Location(Location.get_next_id(), name, latitude, longitude, user_id)
        database.execute(
            "INSERT INTO locations (id, name, latitude, longitude, user_id) VALUES(?, ?, ?, ?, ?)",
            tuple(location.__dict__.values())
        )
        database.commit()

        return location

    @staticmethod
    def get_all_locations() -> list["Location"]:
        return [Location(*r) for r in database.execute("SELECT * FROM locations").fetchall()]

    @staticmethod
    def get_location_by_id(location_id: int) -> "Location":
        res = [l for l in Location.get_all_locations() if l.id == location_id]

        return None if len(res) == 0 else res[0]

    @staticmethod
    def get_next_id() -> int:
        return max([s.id for s in Location.get_all_locations()], default=0) + 1


from session import Session