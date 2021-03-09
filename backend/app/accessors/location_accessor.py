from app.models.location import Location, LocationKey # noqa
from app.models.land_use_type import SpecificLandUseTypeEnum # noqa
import logging

log = logging.getLogger('root')


class LocationAccessor:
    def __init__(self, graph):
        self.graph = graph

    # location_key is defined by namedtuple('LocationKey', ['block', 'road'', 'postal_code, 'floor', 'unit'])
    def get_location_by_key(self, location_key: LocationKey):
        log.info(f"Retrieving location with location key {location_key}")

        tx = self.graph.begin()
        location = tx.run(
            "MATCH  (l: Location) "
            "WHERE  l.block         =   $block "
            "AND    l.road          =   $road "
            "AND    l.postal_code   =   $postal_code "
            "AND    l.floor         =   $floor "
            "AND    l.unit          =   $unit "
            "RETURN l",
            block=location_key.block,
            road=location_key.road,
            postal_code=location_key.postal_code,
            floor=location_key.floor,
            unit=location_key.unit
        ).evaluate()

        if location is None:
            log.warning(f"Location with {location_key} does not exist.")
        else:
            log.info(f"Retrieved location with location key {location_key}")
        tx.commit()
        return location

    # def get_locations_related_to_land_use_type(self, land_use_type: SpecificPropTypeEnum):
    #     # MATCH ( (p: SpecificPropType) {name: $land_use_type})--(l: Location) RETURN l
    #     raise NotImplementedError

    def insert(self, location: Location, location_key: LocationKey):
        if self.get_location_by_key(location_key) is not None:
            raise Exception(f"Location key {location_key} already exists.")

        log.info(f"Inserting location with key {location_key}")
        log.debug(f"Location fields: {location}")

        tx = self.graph.begin()
        insert_location_id = tx.run(
            "CREATE (l: Location) "
            "SET    l.block             =   $block, "
            "       l.road              =   $road, "
            "       l.postal_code       =   $postal_code, "
            "       l.floor             =   $floor, "
            "       l.unit              =   $unit, "
            "       l.building          =   $building, "
            "       l.lot_number        =   $lot_number, "
            "       l.is_shophouse      =   $is_shophouse "
            "RETURN id(l)",
            block=location.block,
            road=location.road,
            postal_code=location.postal_code,
            floor=location.floor,
            unit=location.unit,
            building=location.building,
            lot_number=location.lot_number,
            is_shophouse=location.is_shophouse
        ).evaluate()
        tx.commit()

        log.info(f"Successfully inserted location with node id {insert_location_id}")

        return insert_location_id

    def insert_has_land_use_type_relation(self, location_key: LocationKey, land_use_type_name: str):
        if self.get_location_by_key(location_key) is None:
            raise Exception(f"Location {location_key} does not exist.")
        log.info(f"Inserting HAS_LAND_USE_TYPE relation for location {location_key} and land use type {land_use_type_name}")
        tx = self.graph.begin()
        insert_has_land_use_type_relation_id = tx.run("MATCH (l: Location), (p: SpecificLandUseType) "
                                                      "WHERE l.postal_code=$postal_code AND l.floor=$floor AND l.unit=$unit AND p.name=$name "
                                                      "CREATE (l)-[r: HAS_LAND_USE_TYPE]->(p) "
                                                      "RETURN id(r)",
                                                      block=location_key.block,
                                                      road=location_key.road,
                                                      postal_code=location_key.postal_code,
                                                      floor=location_key.floor,
                                                      unit=location_key.unit,
                                                      name=land_use_type_name).evaluate()

        tx.commit()
        log.info(f"Successfully inserted HAS_LAND_USE_TYPE relation for location {location_key} and land use type {land_use_type_name}")
        return insert_has_land_use_type_relation_id

    def update(self, location: Location, location_key: LocationKey):
        if self.get_location_by_key(location_key) is None:
            raise Exception(f"Location key {location_key} does not exist.")

        log.info(f"Updating location with key {location_key}")
        log.debug(f"Location fields: {location}")

        tx = self.graph.begin()
        update_location_id = tx.run(
            "MATCH  (l: Location) "
            "WHERE  l.block             =   $block, "
            "       l.road              =   $road, "
            "       l.postal_code       =   $postal_code "
            "       l.floor             =   $floor "
            "       l.unit              =   $unit "
            "SET    l.building          =   $building, "
            "       l.lot_number        =   $lot_number, "
            "       l.is_shophouse      =   $is_shophouse "
            "RETURN id(l)",
            block=location.block,
            road=location.road,
            postal_code=location.postal_code,
            floor=location.floor,
            unit=location.unit,
            building=location.building,
            lot_number=location.lot_number,
            is_shophouse=location.is_shophouse
        ).evaluate()
        tx.commit()

        log.info(f"Successfully updated location with node id {update_location_id}")

        return update_location_id

    def delete(self, location_key: LocationKey):
        if self.get_location_by_key(location_key) is None:
            raise Exception(f"Location {location_key} does not exist.")

        log.info(f"Deleting location with location key {location_key}")

        tx = self.graph.begin()
        tx.run(
            "MATCH  (l: Location) "
            "WHERE  l.block         =$block, "
            "       l.road          =$road, "
            "       l.postal_code   =$postal_code, "
            "       l.floor         =$floor, "
            "       l.unit          =$unit "
            "DETACH DELETE l",
            block=location_key.block,
            road=location_key.road,
            postal_code=location_key.postal_code,
            floor=location_key.floor,
            unit=location_key.unit
        ).evaluate()
        tx.commit()

        log.info(f"Successfully deleted location with location key {location_key}")

