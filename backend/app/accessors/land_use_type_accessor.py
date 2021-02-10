from app.models.land_use_type import GenericLandUseType, SpecificLandUseType, GenericLandUseTypeEnum, SpecificLandUseTypeEnum # noqa
from app.models.location import LocationKey # noqa
import logging

log = logging.getLogger('root')

class LandUseTypeAccessor:
    def __init__(self, graph):
        self.graph = graph

    def get_all_generic(self):
        log.info("Retrieving all generic land use types")
        tx = self.graph.begin()
        land_use_types = tx.run("MATCH (p: GenericLandUseType) RETURN p").evaluate()
        log.info("Retrieved all generic land use types")
        log.debug(land_use_types)
        return land_use_types

    def get_all_specific(self):
        log.info("Retrieving all specific land use types")
        tx = self.graph.begin()
        land_use_types = tx.run("MATCH (p: SpecificLandUseType) RETURN p").evaluate()
        log.info("Retrieved all specific land use types")
        log.debug(land_use_types)
        return land_use_types

    def get_specific_by_generic(self, generic_land_use_type: str):
        log.info(f"Retrieving all specific land use type for {generic_land_use_type}")
        tx = self.graph.begin()
        land_use_types = tx.run("MATCH (:GenericLandUseType {name: $generic_land_use_type})--(s: SpecificLandUseType) RETURN s",
                             generic_land_use_type=generic_land_use_type).evaluate()
        log.info(f"Retrieved all specific land use types for {generic_land_use_type}")
        log.debug(land_use_types)
        return land_use_types

    def get_specific_by_name(self, land_use_type_name: str):
        log.info(f"Retrieving specific land use type {land_use_type_name}")
        tx = self.graph.begin()
        land_use_type = tx.run("MATCH (p: SpecificLandUseType) WHERE p.name=$name RETURN p", name=land_use_type_name).evaluate()
        log.info(f"Retrieved specific land use type {land_use_type_name}")
        log.debug(land_use_type)
        return land_use_type

    def get_generic_by_name(self, land_use_type_name: str):
        log.info(f"Retrieving generic land use type {land_use_type_name}")
        tx = self.graph.begin()
        land_use_type = tx.run("MATCH (p: GenericLandUseType) WHERE p.name=$name RETURN p", name=land_use_type_name).evaluate()
        log.info(f"Retrieved generic land use type {land_use_type_name}")
        log.debug(land_use_type)
        return land_use_type

    def get_generic_by_specific(self, specific_land_use_type_name: str):
        log.info(f"Retrieving parent of {specific_land_use_type_name}")
        tx = self.graph.begin()
        generic_land_use_type_name = tx.run("MATCH (gp: GenericLandUseType)--(sp: SpecificLandUseType) "
                                            "WHERE sp.name=$name "
                                            "RETURN gp.name",
                                            name=specific_land_use_type_name
                                            ).evaluate()
        log.info(f"Retrieved parent of {specific_land_use_type_name}")
        log.debug(generic_land_use_type_name)
        return generic_land_use_type_name

    def get_specific_by_location(self, location_key: LocationKey):
        log.info(f"Retrieving land use type of {location_key}")
        tx = self.graph.begin()
        specific_land_use_type_name = tx.run("MATCH (l: Location)--(p: SpecificLandUseType) "
                                             "WHERE l.postal_code=$postal_code "
                                             "AND l.floor=$floor "
                                             "AND l.unit=$unit "
                                             "AND l.block=$block "
                                             "AND l.road=$road "
                                             "RETURN p.name",
                                             postal_code=location_key.postal_code,
                                             floor=location_key.floor,
                                             unit=location_key.unit,
                                             block=location_key.block,
                                             road=location_key.road
                                             ).evaluate()
        log.info(f"Retrieved land use type of {location_key}")
        log.debug(specific_land_use_type_name)
        return specific_land_use_type_name

    def create_specific(self, land_use_type: SpecificLandUseType):
        if self.get_specific_by_name(land_use_type.name) is not None:
            raise Exception(f"Specific land use type {land_use_type} already exists.")
        log.info(f"Creating specific land use type {land_use_type.name}")
        tx = self.graph.begin()
        land_use_type_node_id = tx.run("CREATE (p: SpecificLandUseType) SET p.name=$name RETURN id(p)",
                                   name=land_use_type.name).evaluate()
        tx.commit()
        log.info(f"Created specific land use type {land_use_type.name} with node id {land_use_type_node_id}")
        return land_use_type_node_id

    def create_generic(self, land_use_type: GenericLandUseType):
        if self.get_generic_by_name(land_use_type.name) is not None:
            raise Exception(f"Generic land use type {land_use_type} already exists.")
        log.info(f"Creating generic land use type {land_use_type.name}")
        tx = self.graph.begin()
        land_use_type_node_id = tx.run("CREATE (p: GenericLandUseType) SET p.name=$name RETURN id(p)",
                                   name=land_use_type.name).evaluate()
        tx.commit()
        log.info(f"Created generic land use type {land_use_type.name} with node id {land_use_type_node_id}")
        return land_use_type_node_id

    def create_is_a_relation(self, specific: str, generic: str):
        log.info(f"Creating IS_A relation between {specific} and {generic}")
        tx = self.graph.begin()
        is_a_relation_id = tx.run("MATCH (s: SpecificLandUseType), (g: GenericLandUseType) "
                                  "WHERE s.name=$specific AND g.name=$generic "
                                  "CREATE (s)-[r: IS_A]->(g) RETURN id(r)",
                                  specific=specific,
                                  generic=generic).evaluate()
        tx.commit()
        log.info(f"Created IS_A relation between {specific} and {generic} with id {is_a_relation_id}")
        return is_a_relation_id

    # TODO: finish implementing the function after model is updated
    def update_specific(self, land_use_type: SpecificLandUseType):
        if self.get_specific_by_name(land_use_type.name) is None:
            raise Exception(f"Specific land use type {land_use_type} does not exist.")
        log.info(f"Updating specific land use type {land_use_type.name}")
        log.debug(land_use_type)
        tx = self.graph.begin()
        land_use_type_node_id = tx.run("MATCH (p: SpecificLandUseType) WHERE p.name=$name SET <KEY=VALUE>",
                                   name=land_use_type.name).evaluate()
        tx.commit()
        log.info(f"Updated specific land use type {land_use_type.name}, node id {land_use_type_node_id}")
        return land_use_type_node_id

    # TODO: finish implementing the function after model is updated
    def update_generic(self, land_use_type: GenericLandUseType):
        if self.get_generic_by_name(land_use_type.name) is None:
            raise Exception(f"Generic land use type {land_use_type} does not exist.")
        log.info(f"Updating generic land use type {land_use_type.name}")
        log.debug(land_use_type)
        tx = self.graph.begin()
        land_use_type_node_id = tx.run("MATCH (p: GenericLandUseType) WHERE p.name=$name SET <KEY=VALUE>",
                                   name=land_use_type.name).evaluate()
        tx.commit()
        log.info(f"Updated generic land use type {land_use_type.name}, node id {land_use_type_node_id}")
        return land_use_type_node_id

    def delete_specific(self, name: str):
        if self.get_specific_by_name(name) is None:
            raise Exception(f"Specific land use type {name} does not exist.")
        log.info(f"Deleting specific land use type{name}")
        tx = self.graph.begin()
        tx.run("MATCH (p: SpecificLandUseType) WHERE p.name=$name DETACH DELETE p", name=name).evaluate()
        log.info(f"Successfully deleted specific land use type {name}")
        tx.commit()

    def delete_generic(self, name: str):
        if self.get_generic_by_name(name) is None:
            raise Exception(f"Generic land use type {name} does not exist.")
        log.info(f"Deleting generic land use type{name}")
        tx = self.graph.begin()
        tx.run("MATCH (u: GenericLandUseType) WHERE p.name=$name DETACH DELETE p", name=name).evaluate()
        log.info(f"Successfully deleted generic land use type {name}")
        tx.commit()

