from typing import NamedTuple
from app.models.location import Location, LocationKey # noqa
from app.models.property_type import SpecificPropTypeEnum # noqa
from collections import namedtuple
import logging

log = logging.getLogger('root')


class LocationAccessor:
    def __init__(self, graph):
        self.graph = graph
    # location_key is defined by namedtuple('LocationKey', ['postal_code', 'floor', 'unit'])
    def get_location_by_key(self, location_key: LocationKey):
        tx = self.graph.begin()
        log.info(f"Retrieving location with location key {location_key}")
        location = tx.run("MATCH (l: Location) WHERE l.postal_code=$postal_code, l.floor=$floor, l.unit=$unit RETURN l",
                          postal_code=location_key.postal_code,
                          floor=location_key.floor,
                          unit=location_key.unit
                          ).evaluate()
        if location is None:
            log.warning(f"Location with {location_key} does not exist.")
        log.info(f"Retrieved location with location key {location_key}")
        return location

    def get_locations_related_to_prop_type(self, prop_type: SpecificPropTypeEnum):
        # MATCH ( (p: SpecificPropType) {name: $prop_type})--(l: Location) RETURN l
        raise NotImplementedError

    def insert(self, location: Location):
        location_key = namedtuple('LocationKey', location.postal_code, location.floor, location.unit)
        if self.get_location_by_key(location_key) is not None:
            raise Exception(f"Location key {location_key} already exists.")
        log.info(f"Inserting location with key {location_key}")
        log.debug(f"Location fields: {location}")
        tx = self.graph.begin()
        insert_location_id = tx.run("CREATE (l: Location) SET l.postal_code=$postal_code, l.floor=$floor, l.unit=$unit, l.lot_number=$lot_number, l.building_name=$building_name RETURN id(l)",
               postal_code=location.postal_code,
               floor=location.floor,
               unit=location.unit,
               lot_number=location.lot_number,
               buiilding_name=location.buiilding_name
               ).evaluate()
        tx.commit()
        log.info(f"Successfully inserted location with node id {insert_location_id}")
        return insert_location_id

    def insert_has_prop_type_relation(self, location_key: LocationKey, prop_type_name: str):
        if self.get_location_by_key(location_key) is None:
            raise Exception(f"Location {location_key} does not exist.")
        log.info(f"Inserting HAS_PROP_TYPE relation for location {location_key} and property type {prop_type_name}")
        tx = self.graph.begin()
        insert_has_prop_type_relation_id = tx.run("MATCH (l: Location), (p: SpecificPropType) "
                                                  "WHERE l.postal_code=$postal_code AND l.floor=$floor AND l.unit=$unit AND p.name=$name "
                                                  "CREATE (l)-[r: HAS_PROP_TYPE]->(p) "
                                                  "RETURN id(r)",
                                                  postal_code=location_key.postal_code,
                                                  floor=location_key.floor,
                                                  unit=location_key.unit,
                                                  name=prop_type_name).evaluate()

        tx.commit()
        log.info(f"Successfully inserted HAS_PROP_TYPE relation for location {location_key} and property type {prop_type_name}")
        return insert_has_prop_type_relation_id


    def update(self, location: Location):
        location_key = namedtuple('LocationKey', location.postal_code, location.floor, location.unit)
        if self.get_location_by_key(location_key) is None:
            raise Exception(f"Location key {location_key} does not exist.")
        log.info(f"Updating location with key {location_key}")
        log.debug(f"Location fields: {location}")
        tx = self.graph.begin()
        update_location_id = tx.run(
            "MATCH (l: Location) WHERE l.postal_code=$postal_code, l.floor=$floor, l.unit=$unit SET l.lot_number=$lot_number, l.building_name=$building_name RETURN id(l)",
            postal_code=location.postal_code,
            floor=location.floor,
            unit=location.unit,
            lot_number=location.lot_number,
            buiilding_name=location.buiilding_name
            ).evaluate()
        tx.commit()
        log.info(f"Successfully updated location with node id {update_location_id}")
        return update_location_id

    def delete(self, location_key: NamedTuple):
        if self.get_location_by_key(location_key) is None:
            raise Exception(f"Location {location_key} does not exist.")
        log.info(f"Deleting location with location key {location_key}")
        tx = self.graph.begin()
        tx.run("MATCH (l: Location) WHERE l.postal_code=$postal_code, l.floor=$floor, l.unit=$unit DETACH DELETE l",
               postal_code=location.postal_code,
               floor=location.floor,
               unit=location.unit
               ).evaluate()
        log.info(f"Successfully deleted location with location key {location_key}")
        tx.commit()

