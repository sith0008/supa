from app.models.property_type import GenericPropType, SpecificPropType, GenericPropTypeEnum, SpecificPropTypeEnum # noqa
from app.models.location import LocationKey # noqa
import logging

log = logging.getLogger('root')

class PropertyTypeAccessor:
    def __init__(self, graph):
        self.graph = graph

    def get_all_generic(self):
        log.info("Retrieving all generic property types")
        tx = self.graph.begin()
        property_types = tx.run("MATCH (p: GenericPropType) RETURN p").evaluate()
        log.info("Retrieved all generic property types")
        log.debug(property_types)
        return property_types

    def get_all_specific(self):
        log.info("Retrieving all specific property types")
        tx = self.graph.begin()
        property_types = tx.run("MATCH (p: SpecificPropType) RETURN p").evaluate()
        log.info("Retrieved all specific property types")
        log.debug(property_types)
        return property_types

    def get_specific_by_generic(self, generic_property_type: str):
        log.info(f"Retrieving all specific property type for {generic_property_type}")
        tx = self.graph.begin()
        property_types = tx.run("MATCH (:GenericPropType {name: $generic_property_type})--(s: SpecificPropType) RETURN s",
                             generic_property_type=generic_property_type).evaluate()
        log.info(f"Retrieved all specific property types for {generic_property_type}")
        log.debug(property_types)
        return property_types

    def get_specific_by_name(self, property_type_name: str):
        log.info(f"Retrieving specific property type {property_type_name}")
        tx = self.graph.begin()
        property_type = tx.run("MATCH (p: SpecificPropType) WHERE p.name=$name RETURN p", name=property_type_name).evaluate()
        log.info(f"Retrieved specific property type {property_type_name}")
        log.debug(property_type)
        return property_type

    def get_generic_by_name(self, property_type_name: str):
        log.info(f"Retrieving generic property type {property_type_name}")
        tx = self.graph.begin()
        property_type = tx.run("MATCH (p: GenericPropType) WHERE p.name=$name RETURN p", name=property_type_name).evaluate()
        log.info(f"Retrieved generic property type {property_type_name}")
        log.debug(property_type)
        return property_type

    def get_generic_by_specific(self, specific_property_type_name: str):
        log.info(f"Retrieving parent of {specific_property_type_name}")
        tx = self.graph.begin()
        generic_property_type_name = tx.run("MATCH (gp: GenericPropType)--(sp: SpecificPropType) "
                                            "WHERE sp.name=$name "
                                            "RETURN gp.name",
                                            name=specific_property_type_name
                                            ).evaluate()
        log.info(f"Retrieved parent of {specific_property_type_name}")
        log.debug(generic_property_type_name)
        return generic_property_type_name

    def get_specific_by_location(self, location_key: LocationKey):
        log.info(f"Retrieving property type of {location_key}")
        tx = self.graph.begin()
        specific_property_type_name = tx.run("MATCH (l: Location)--(p: SpecificPropType) "
                                             "WHERE l.postal_code=$postal_code AND l.floor=$floor AND l.unit=$unit"
                                             "RETURN p.name",
                                             postal_code=location_key.postal_code,
                                             floor=location_key.floor,
                                             unit=location_key.unit
                                             ).evaluate()
        log.info(f"Retrieved property type of {location_key}")
        log.debug(specific_property_type_name)
        return specific_property_type_name

    def create_specific(self, property_type: SpecificPropType):
        if self.get_specific_by_name(property_type.name) is not None:
            raise Exception(f"Specific property type {property_type} already exists.")
        log.info(f"Creating specific property type {property_type.name}")
        tx = self.graph.begin()
        property_type_node_id = tx.run("CREATE (p: SpecificPropType) SET p.name=$name RETURN id(p)",
                                   name=property_type.name).evaluate()
        tx.commit()
        log.info(f"Created specific property type {property_type.name} with node id {property_type_node_id}")
        return property_type_node_id

    def create_generic(self, property_type: GenericPropType):
        if self.get_generic_by_name(property_type.name) is not None:
            raise Exception(f"Generic property type {property_type} already exists.")
        log.info(f"Creating generic property type {property_type.name}")
        tx = self.graph.begin()
        property_type_node_id = tx.run("CREATE (p: GenericPropType) SET p.name=$name RETURN id(p)",
                                   name=property_type.name).evaluate()
        tx.commit()
        log.info(f"Created generic property type {property_type.name} with node id {property_type_node_id}")
        return property_type_node_id

    def create_is_a_relation(self, specific: str, generic: str):
        log.info(f"Creating IS_A relation between {specific} and {generic}")
        tx = self.graph.begin()
        is_a_relation_id = tx.run("MATCH (s: SpecificPropType), (g: GenericPropType) "
                                  "WHERE s.name=$specific AND g.name=$generic "
                                  "CREATE (s)-[r: IS_A]->(g) RETURN id(r)",
                                  specific=specific,
                                  generic=generic).evaluate()
        tx.commit()
        log.info(f"Created IS_A relation between {specific} and {generic} with id {is_a_relation_id}")
        return is_a_relation_id

    # TODO: finish implementing the function after model is updated
    def update_specific(self, property_type: SpecificPropType):
        if self.get_specific_by_name(property_type.name) is None:
            raise Exception(f"Specific property type {property_type} does not exist.")
        log.info(f"Updating specific property type {property_type.name}")
        log.debug(property_type)
        tx = self.graph.begin()
        property_type_node_id = tx.run("MATCH (p: SpecificPropType) WHERE p.name=$name SET <KEY=VALUE>",
                                   name=property_type.name).evaluate()
        tx.commit()
        log.info(f"Updated specific property type {property_type.name}, node id {property_type_node_id}")
        return property_type_node_id

    # TODO: finish implementing the function after model is updated
    def update_generic(self, property_type: GenericPropType):
        if self.get_generic_by_name(property_type.name) is None:
            raise Exception(f"Generic property type {property_type} does not exist.")
        log.info(f"Updating generic property type {property_type.name}")
        log.debug(property_type)
        tx = self.graph.begin()
        property_type_node_id = tx.run("MATCH (p: GenericPropType) WHERE p.name=$name SET <KEY=VALUE>",
                                   name=property_type.name).evaluate()
        tx.commit()
        log.info(f"Updated generic property type {property_type.name}, node id {property_type_node_id}")
        return property_type_node_id

    def delete_specific(self, name: str):
        if self.get_specific_by_name(name) is None:
            raise Exception(f"Specific property type {name} does not exist.")
        log.info(f"Deleting specific property type{name}")
        tx = self.graph.begin()
        tx.run("MATCH (p: SpecificPropType) WHERE p.name=$name DETACH DELETE p", name=name).evaluate()
        log.info(f"Successfully deleted specific property type {name}")
        tx.commit()

    def delete_generic(self, name: str):
        if self.get_generic_by_name(name) is None:
            raise Exception(f"Generic property type {name} does not exist.")
        log.info(f"Deleting generic property type{name}")
        tx = self.graph.begin()
        tx.run("MATCH (u: GenericPropType) WHERE p.name=$name DETACH DELETE p", name=name).evaluate()
        log.info(f"Successfully deleted generic property type {name}")
        tx.commit()

