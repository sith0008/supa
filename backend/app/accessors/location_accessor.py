from typing import NamedTuple
from app.models.location import Location # noqa


class LocationAccessor:
    def __init__(self, graph):
        self.graph = graph
    # location is keyed by postal code, floor, unit
    def get_location_by_key(self, location_key: NamedTuple):
        raise NotImplementedError

    def insert(self, location: Location):
        raise NotImplementedError

    def update(self, location: Location):
        raise NotImplementedError

    def delete(self, location_key: NamedTuple):
        raise NotImplementedError