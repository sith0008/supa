from app.accessors.location_accessor import LocationAccessor # noqa
from app.models.location import Location, LocationKey # noqa
from typing import Dict, NamedTuple

class LocationService:
    def __init__(self, graph):
        self.graph = graph
        self.location_accessor = LocationAccessor(graph)

    def has_full_location_key(self, m: Dict):
        return "postal_code" in m and "floor" in m and "unit" in m

    def get_location(self, filter_map: Dict):
        if self.has_full_location_key(filter_map):
            location_key = LocationKey(filter_map["postal_code"], filter_map["floor"], filter_map["unit"])
            location = self.location_accessor.get_location_by_key(location_key)
            return location
        else:
            # TODO: add support for retrieving location by Zone, PTA, AGU etc (pending location data model update)
            raise NotImplementedError

    def insert_location(self, fields_map: Dict):
        new_location = Location()
        for k, v in fields_map.items():
            setattr(new_location, k, v)
        return self.location_accessor.insert(new_location)

    def update_location(self, fields_map: Dict):
        new_location = Location()
        for k, v in fields_map.items():
            setattr(new_location, k, v)
        return self.location_accessor.update(new_location)

    def delete_location(self, fields_map: Dict):
        if self.has_full_location_key(fields_map):
            location_key = LocationKey(fields_map["postal_code"], fields_map["floor"], fields_map["unit"])
            self.location_accessor.delete(location_key)
        else:
            raise NotImplementedError

    # TODO: add is_pta, is_agu, is_pa methods
