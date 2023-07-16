import requests
from typing import Union

from models.model import Model


class Location(Model):
    table = "locations"

    def __init__(self, id: int, name: str, latitude: float, longitude: float, user_id: int, geo_data: Union[str, None],
                 cover_image: Union[bytes, None]) -> None:
        super().__init__(id)
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.user_id = user_id
        self.geo_data = geo_data if geo_data else self.fetch_geo_data()
        self.cover_image = cover_image

    def fetch_geo_data(self) -> str:
        res = requests.get(f"https://api.bigdatacloud.net/data/reverse-geocode-client?latitude={self.latitude}&longitude={self.longitude}")
        data = res.json()

        return f"{data['city']},{ data['countryName']}"
