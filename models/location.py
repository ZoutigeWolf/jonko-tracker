import requests

from database import database


class Location:
    def __init__(self, id: int, name: str, latitude: float, longitude: float, user_id: int, geo_data: str | None,
                 cover_image: bytes) -> None:
        self.id = id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.user_id = user_id
        self.geo_data = geo_data if geo_data else self.fetch_geo_data()
        self.cover_image = cover_image

    def update(self, name: str = None, latitude: float = None, longitude: float = None, cover_image: bytes = None) -> None:
        if name is not None:
            self.name = name

        if latitude is not None:
            self.latitude = latitude

        if longitude is not None:
            self.longitude = longitude

        if cover_image is not None:
            self.cover_image = cover_image

        self.geo_data = self.fetch_geo_data()

        database.execute(
            "UPDATE locations SET name = ?, latitude = ?, longitude = ?, geo_data = ?, cover_image = ? WHERE id = ?",
            (self.name, self.latitude, self.longitude, self.geo_data, self.cover_image, self.id)
        )
        database.commit()

    def delete(self) -> None:
        database.execute("DELETE FROM locations WHERE id = ?", (self.id,))
        database.commit()

    def fetch_geo_data(self) -> str:
        res = requests.get(f"https://api.bigdatacloud.net/data/reverse-geocode-client?latitude={self.latitude}&longitude={self.longitude}")
        data = res.json()

        return f"{data['city']},{ data['countryName']}"

    @staticmethod
    def create_location(name: str, latitude: float, longitude: float, user_id: int, cover_image: bytes) -> "Location":
        location = Location(Location.get_next_id(), name, latitude, longitude, user_id, None, cover_image)

        database.execute(
            """
            INSERT INTO locations (id, name, latitude, longitude, user_id, geo_data, cover_image)
            VALUES(?, ?, ?, ?, ?, ?, ?)
            """,
            tuple(location.__dict__)
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


from models.session import Session