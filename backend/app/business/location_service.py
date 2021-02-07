from app.accessors.location_accessor import LocationAccessor # noqa
from app.models.location import Location, LocationKey # noqa
from typing import Dict


class LocationService:
    def __init__(self, graph):
        self.graph = graph
        self.location_accessor = LocationAccessor(graph)

    @staticmethod
    def has_full_location_key(m: Dict):
        return \
            "block" in m and \
            "road" in m and \
            "postal_code" in m and \
            "floor" in m and \
            "unit" in m

    def get_location(self, filter_map: Dict):
        if self.has_full_location_key(filter_map):
            location_key = LocationKey(
                filter_map["block"],
                filter_map["road"],
                filter_map["postal_code"],
                filter_map["floor"],
                filter_map["unit"]
            )
            location = self.location_accessor.get_location_by_key(location_key)
            return location
        else:
            # TODO: add support for retrieving location by Zone, PTA, AGU etc (pending location data model update)
            raise NotImplementedError

    def insert_location(self, fields_map: Dict):
        new_location = Location()
        for k, v in fields_map.items():
            setattr(new_location, k, v)
        location_key = LocationKey(
            fields_map["block"],
            fields_map["road"],
            fields_map["postal_code"],
            fields_map["floor"],
            fields_map["unit"]
        )
        setattr(new_location, 'is_shophouse', self.isShophouse(location_key))
        setattr(new_location, 'is_hdb_commercial', self.isHDBCommercial(location_key))
        insert_location_id = self.location_accessor.insert(new_location)
        self.location_accessor.insert_has_prop_type_relation(location_key, self.landUse(location_key))
        return insert_location_id

    def update_location(self, fields_map: Dict):
        new_location = Location()
        for k, v in fields_map.items():
            setattr(new_location, k, v)
        location_key = LocationKey(
            fields_map["block"],
            fields_map["road"],
            fields_map["postal_code"],
            fields_map["floor"],
            fields_map["unit"]
        )
        setattr(new_location, 'is_shophouse', self.isShophouse(location_key))
        setattr(new_location, 'is_hdb_commercial', self.isHDBCommercial(location_key))
        return self.location_accessor.update(new_location)

    def delete_location(self, fields_map: Dict):
        if self.has_full_location_key(fields_map):
            location_key = LocationKey(
                fields_map["block"],
                fields_map["road"],
                fields_map["postal_code"],
                fields_map["floor"],
                fields_map["unit"]
            )
            self.location_accessor.delete(location_key)
        else:
            raise NotImplementedError

    def landUse(self, location_key):
        # TODO: implement function
        return "None"

    def isShophouse(self, location_key):
        # TODO: implement function
        return False

    def isHDBCommercial(self, location_key):
        # TODO: implement function
        return False

    # TODO: add is_pta, is_agu, is_pa methods
