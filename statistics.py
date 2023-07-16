from models.user import User
from models.session import Session
from models.location import Location


class Statistics:
    def __init__(self, user: User):
        self.user = user

    def get_data(self) -> list:
        return [
            {
                "title": "Most common locations",
                "data": [l.name for l in self.most_common_locations()]
            }
        ]

    def most_common_locations(self) -> list[Location]:
        sessions = self.user.get_sessions()

        count = {}

        for s in sessions:
            if s.location_id in count:
                count[s.location_id] += 1

            else:
                count[s.location_id] = 1

        max_count = max(count.values())

        return [Location.get_by("id", i) for i, c in count.items() if c == max_count]
