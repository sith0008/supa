from app.accessors.location_accessor import LocationAccessor # noqa
from app.accessors.postal_code_accessor import PostalCodeAccessor # noqa
from app.models.location import Location, LocationKey # noqa
from sqlalchemy.orm import sessionmaker
from typing import Dict
import json


class LocationService:
    def __init__(self, graph, engine):
        self.graph = graph
        self.location_accessor = LocationAccessor(graph)
        self.engine = engine

    @staticmethod
    def has_full_location_key(m: Dict):
        return \
            "block" in m and \
            "road" in m and \
            "postal_code" in m and \
            "floor" in m and \
            "unit" in m

    def get_address(self, filter_map: Dict):
        if 'postal_code' in filter_map:
            postal_code = filter_map['postal_code']
            with open('app/models/postal_codes.json') as f:
                data = json.load(f)
            return [{'block': x['BLK_NO'],
                     'road': x['ROAD_NAME'],
                     'building': x['BUILDING'] if x['BUILDING'] != 'NIL' else None,
                     'postal_code': postal_code
                     }
                    for x in data[postal_code]
                    if 'BLK_NO' in x and
                    'ROAD_NAME' in x and
                    'BUILDING' in x
                    ]
        else:
            # TODO: add support for retrieving location by Zone, PTA, AGU etc (pending location data model update)
            raise NotImplementedError

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

        setattr(new_location, 'is_shophouse', self.is_shophouse(location_key))
        insert_location_id = self.location_accessor.insert(new_location, location_key)
        self.location_accessor.insert_has_land_use_type_relation(location_key, self.get_land_use_from_location(location_key))

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

        setattr(new_location, 'is_shophouse', self.is_shophouse(location_key))
        return self.location_accessor.update(new_location, location_key)

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

    def get_land_use_from_location(self, location_key: LocationKey):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        accessor = PostalCodeAccessor(session)

        postal_code = accessor.read(
            {
                "block": location_key.block,
                "road": location_key.road,
                "postal_code": location_key.postal_code
            }
        )

        session.close()

        return postal_code[0]["land_use_type"]

    def get_coordinates(self, location_key: LocationKey):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        accessor = PostalCodeAccessor(session)

        postal_code = accessor.read(
            {
                "block": location_key.block,
                "road": location_key.road,
                "postal_code": location_key.postal_code
            }
        )

        session.close()

        return postal_code[0]["latitude"], postal_code[0]["longitude"]

    def is_shophouse(self, location_key: LocationKey):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        accessor = PostalCodeAccessor(session)

        postal_code = accessor.read(
            {
                "block": location_key.block,
                "road": location_key.road,
                "postal_code": location_key.postal_code
            }
        )

        session.close()

        if postal_code and postal_code[0]["property_type"] == 'Shophouses':
            return True
        else:
            return False

    # TODO: add is_pta, is_agu, is_pa methods
