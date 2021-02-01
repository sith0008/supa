from app.accessors.cases_accessor import CasesAccessor # noqa
from app.accessors.location_accessor import LocationAccessor # noqa
from app.accessors.use_class_accessor import UseClassAccessor # noqa
from app.models.past_case import PastCase # noqa
from app.models.location import Location, LocationKey # noqa
from typing import Dict
import logging
from collections import namedtuple

log = logging.getLogger('root')


class CasesService:
    def __init__(self, graph):
        self.graph = graph
        self.cases_accessor = CasesAccessor(graph)
        self.location_accessor = LocationAccessor(graph)
        self.use_class_accessor = UseClassAccessor(graph)

    def get_case(self, filter_map: Dict):
        if "case_id" in filter_map:
            past_case = self.cases_accessor.get_case_by_id(filter_map["case_id"])
            return past_case
        else:
            raise NotImplementedError

    def get_similar_case_exact(self, use_class, property_type):
        log.info(f"Retrieving past cases with use class {use_class} and property type {property_type}")
        tx = self.graph.begin()
        similar_cases_results = tx.run("MATCH (c:PastCase)--(l:Location)--(p:SpecificPropType), "
                                       "(c:PastCase)--(u:SpecificUseClass) "
                                       "WHERE p.name=$property_type AND u.name=$use_class "
                                       "LIMIT 5 "
                                       "RETURN c, l",
                                       property_type=property_type,
                                       use_class=use_class
                                       ).evaluate()
        log.info(f"Retrieved {len(similar_cases_results)} past cases with use class {use_class} and property type {property_type}")
        return similar_cases_results

    def get_similar_case_extended(self,
                                  specific_use_class,
                                  generic_use_class,
                                  specific_property_type,
                                  generic_property_type,
                                  ):
        log.info(f"Retrieving past cases with generic use class {generic_use_class} and generic property type {generic_property_type}")
        tx = self.graph.begin()
        similar_cases_results= tx.run("MATCH (c:PastCase)--(l:Location)--(sp:SpecificPropType)--(gp:GenericPropType), "
                                      "(c:PastCase)--(su:SpecificUseClass)--(gu:GenericUseClass) "
                                      "WHERE NOT (sp.name=$specific_property_type AND su.name=$specific_use_class) "
                                      "AND (gp.name=$generic_property_type AND gu.name=$generic_use_class) "
                                      "LIMIT 5"
                                      "RETURN c, l, sp, gp, su, gu",
                                      specific_property_type=specific_property_type,
                                      generic_property_type=generic_property_type,
                                      specific_use_class=specific_use_class,
                                      generic_use_class=generic_use_class,
                                      ).evaluate()
        log.info(f"Retrieved {len(similar_cases_results)} past cases with generic use class {generic_use_class} and generic property type {generic_property_type}")
        return similar_cases_results


    def insert_case_with_location(self, case_fields: Dict, location_fields: Dict, use_class_name: str):
        if not self.use_class_accessor.get_specific_by_name(use_class_name):
            log.error(f"Use class {use_class_name} does not exist in database.")
            raise NotImplementedError

        location_key = LocationKey(
            location_fields["postal_code"],
            location_fields["floor"],
            location_fields["unit"]
        )

        if not self.location_accessor.get_location_by_key(location_key):
            log.error(f"Location {location_key} does not exist in database.")
            raise Exception("Location does not exist")

        new_case = PastCase()
        for k, v in case_fields.items():
            setattr(new_case, k, v)
        insert_case_node_id = self.cases_accessor.insert(new_case)
        insert_has_use_class_relation_id = self.cases_accessor.insert_has_use_class_relation(new_case.case_id, use_class_name)
        insert_located_in_relation_id = self.cases_accessor.insert_located_in_relation(new_case.case_id, location_key)
        return insert_case_node_id

    def update_case(self, fields_map: Dict):
        new_case = PastCase()
        for k, v in fields_map.items():
            setattr(new_case, k, v)
        return self.cases_accessor.update(new_case)

    def delete_case(self, case_id: str):
        self.cases_accessor.delete(case_id)
