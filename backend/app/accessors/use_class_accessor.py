from app.models.past_case import PastCase # noqa
from app.models.use_class import SpecificUseClass, GenericUseClass, SpecificUseClassEnum, GenericUseClassEnum # noqa
import logging

log = logging.getLogger('root')

class UseClassAccessor:
    def __init__(self, graph):
        self.graph = graph

    def get_all_generic(self):
        log.info("Retrieving all generic use classes")
        tx = self.graph.begin()
        use_classes = tx.run("MATCH (u: GenericUseClass) RETURN u").evaluate()
        log.info("Retrieved all generic use classes")
        log.debug(use_classes)
        return use_classes

    def get_all_specific(self):
        log.info("Retrieving all specific use classes")
        tx = self.graph.begin()
        use_classes = tx.run("MATCH (u: SpecificUseClass) RETURN u").evaluate()
        log.info("Retrieved all specific use classes")
        log.debug(use_classes)
        return use_classes

    def get_specific_by_generic(self, generic_use_class: str):
        log.info(f"Retrieving all specific use classes for {generic_use_class}")
        tx = self.graph.begin()
        use_classes = tx.run("MATCH (:GenericUseClass {name: $generic_use_class})--(su: SpecificUseClass) RETURN su", generic_use_class=generic_use_class).evaluate()
        log.info(f"Retrieved all specific use classes for {generic_use_class}")
        log.debug(use_classes)
        return use_classes

    def get_specific_by_name(self, use_class_name: str):
        log.info(f"Retrieving specific use class {use_class_name}")
        tx = self.graph.begin()
        use_class = tx.run("MATCH (u: SpecificUseClass) WHERE u.name=$name RETURN u", name=use_class_name).evaluate()
        log.info(f"Retrieved specific use class {use_class_name}")
        log.debug(use_class)
        return use_class

    def get_generic_by_name(self, use_class_name: str):
        log.info(f"Retrieving generic use class {use_class_name}")
        tx = self.graph.begin()
        use_class = tx.run("MATCH (u: GenericUseClass) WHERE u.name=$name RETURN u", name=use_class_name).evaluate()
        log.info(f"Retrieved generic use class {use_class_name}")
        log.debug(use_class)
        return use_class

    def get_generic_by_specific(self, specific_use_class_name: str):
        log.info(f"Retrieving parent of {specific_use_class_name}")
        tx = self.graph.begin()
        generic_use_class_name = tx.run("MATCH (gu: GenericUseClass)--(su: SpecificUseClass) "
                                        "WHERE su.name=$name "
                                        "RETURN gu.name",
                                        name=specific_use_class_name
                                        ).evaluate()
        log.info(f"Retrieved parent of {specific_use_class_name}")
        log.debug(generic_use_class_name)
        return generic_use_class_name

    def create_specific(self, use_class: SpecificUseClass):
        if self.get_specific_by_name(use_class.name) is not None:
            raise Exception(f"Specific use class {use_class} already exists.")
        log.info(f"Creating specific use class {use_class.name}")
        tx = self.graph.begin()
        use_class_node_id = tx.run("CREATE (u: SpecificUseClass) SET u.name=$name RETURN id(u)", name=use_class.name).evaluate()
        tx.commit()
        log.info(f"Created specific use class {use_class.name} with node id {use_class_node_id}")
        return use_class_node_id

    def create_generic(self, use_class: GenericUseClass):
        if self.get_generic_by_name(use_class.name) is not None:
            raise Exception(f"Generic use class {use_class} already exists.")
        log.info(f"Creating generic use class {use_class.name}")
        tx = self.graph.begin()
        use_class_node_id = tx.run("CREATE (u: GenericUseClass) SET u.name=$name RETURN id(u)",
                                   name=use_class.name).evaluate()
        tx.commit()
        log.info(f"Created generic use class {use_class.name} with node id {use_class_node_id}")
        return use_class_node_id

    def create_is_a_relation(self, specific: str, generic: str):
            # "MATCH (c:Case),(l:Location) WHERE id(c) = $caseId AND id(l) = $locationId CREATE (c)-[r:LOCATED_IN]->(l) RETURN id(r)",
        log.info(f"Creating IS_A relation between {specific} and {generic}")
        tx = self.graph.begin()
        is_a_relation_id = tx.run("MATCH (s: SpecificUseClass), (g: GenericUseClass) "
                                  "WHERE s.name=$specific AND g.name=$generic "
                                  "CREATE (s)-[r: IS_A]->(g) RETURN id(r)",
                                  specific=specific,
                                  generic=generic).evaluate()
        tx.commit()
        log.info(f"Created IS_A relation between {specific} and {generic} with id {is_a_relation_id}")
        return is_a_relation_id

    # TODO: finish implementing the function after model is updated
    def update_specific(self, use_class: SpecificUseClass):
        if self.get_specific_by_name(use_class.name) is None:
            raise Exception(f"Specific use class {use_class} does not exist.")
        log.info(f"Updating specific use class {use_class.name}")
        log.debug(use_class)
        tx = self.graph.begin()
        use_class_node_id = tx.run("MATCH (u: SpecificUseClass) WHERE u.name=$name SET <KEY=VALUE>", name=use_class.name).evaluate()
        tx.commit()
        log.info(f"Updated specific use class {use_class.name}, node id {use_class_node_id}")
        return use_class_node_id

    # TODO: finish implementing the function after model is updated
    def update_generic(self, use_class: GenericUseClass):
        if self.get_generic_by_name(use_class.name) is None:
            raise Exception(f"Generic use class {use_class} does not exist.")
        log.info(f"Updating generic use class {use_class.name}")
        log.debug(use_class)
        tx = self.graph.begin()
        use_class_node_id = tx.run("MATCH (u: GenericUseClass) WHERE u.name=$name SET <KEY=VALUE>",
                                   name=use_class.name).evaluate()
        tx.commit()
        log.info(f"Updated generic use class {use_class.name}, node id {use_class_node_id}")
        return use_class_node_id

    def delete_specific(self, name: str):
        if self.get_specific_by_name(name) is None:
            raise Exception(f"Specific use class {name} does not exist.")
        log.info(f"Deleting specific use class{name}")
        tx = self.graph.begin()
        tx.run("MATCH (u: SpecificUseClass) WHERE u.name=$name DETACH DELETE u", name=name).evaluate()
        log.info(f"Successfully deleted specific use class {name}")
        tx.commit()

    def delete_generic(self, name: str):
        if self.get_generic_by_name(name) is None:
            raise Exception(f"Generic use class {name} does not exist.")
        log.info(f"Deleting generic use class{name}")
        tx = self.graph.begin()
        tx.run("MATCH (u: GenericUseClass) WHERE u.name=$name DETACH DELETE u", name=name).evaluate()
        log.info(f"Successfully deleted generic use class {name}")
        tx.commit()

