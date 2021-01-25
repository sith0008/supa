from typing import NamedTuple
from app.models.location import Location # noqa
from app.models.property_type import SpecificPropTypeEnum # noqa


class LocationAccessor:
    def __init__(self, graph):
        self.graph = graph
    # location is keyed by postal code, floor, unit
    def get_location_by_key(self, location_key: NamedTuple):
        raise NotImplementedError

    def get_locations_related_to_prop_type(self, prop_type: SpecificPropTypeEnum):
        raise NotImplementedError

    def insert(self, location: Location):
        raise NotImplementedError

    def update(self, location: Location):
        raise NotImplementedError

    def delete(self, location_key: NamedTuple):
        raise NotImplementedError

