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

    def get_similar_case_exact(self, use_class, land_use_type):
        log.info(f"Retrieving past cases with use class {use_class} and land_use type {land_use_type}")
        tx = self.graph.begin()
        similar_cases_results = tx.run("MATCH (c:PastCase)--(l:Location)--(lu:SpecificLandUseType), "
                                       "(c:PastCase)--(u:SpecificUseClass) "
                                       "WHERE lu.name=$land_use_type AND u.name=$use_class "
                                       "RETURN c, l "
                                       "LIMIT 5",
                                       land_use_type=land_use_type,
                                       use_class=use_class
                                       ).data()
        # log.debug(similar_cases_results[0])
        if similar_cases_results:
            log.info(f"Retrieved {len(similar_cases_results)} past cases with use class {use_class} and land_use type {land_use_type}")
        else:
            log.info(f"No similar cases found.")
        processed_results = [{"case": res["c"],
                              "location": res["l"],
                              "use_class": {"specific": use_class},
                              "land_use_type": {"specific": land_use_type}}
                             for res in similar_cases_results]
        log.debug(processed_results)
        return processed_results

    def get_similar_case_extended(self,
                                  specific_use_class,
                                  generic_use_class,
                                  specific_land_use_type,
                                  generic_land_use_type,
                                  ):
        log.info(f"Retrieving past cases with generic use class {generic_use_class} and generic land_use type {generic_land_use_type}")
        tx = self.graph.begin()
        similar_cases_results = tx.run("MATCH (c:PastCase)--(l:Location)--(slu:SpecificLandUseType)--(glu:GenericLandUseType), "
                                      "(c:PastCase)--(su:SpecificUseClass)--(gu:GenericUseClass) "
                                      "WHERE NOT (slu.name=$specific_land_use_type AND su.name=$specific_use_class) "
                                      "AND (glu.name=$generic_land_use_type AND gu.name=$generic_use_class) "
                                      "RETURN c, l, su, gu, slu, glu "
                                      "LIMIT 5",
                                      specific_land_use_type=specific_land_use_type,
                                      generic_land_use_type=generic_land_use_type,
                                      specific_use_class=specific_use_class,
                                      generic_use_class=generic_use_class,
                                      ).data()
        if similar_cases_results:
            log.info(f"Retrieved {len(similar_cases_results)} past cases with generic use class {generic_use_class} and generic land_use type {generic_land_use_type}")
        else:
            log.info(f"No similar cases found.")
        processed_results = [{"case": res["c"],
                              "location": res["l"],
                              "use_class": {
                                  "specific": res["su"]["name"],
                                  "generic": res["gu"]["name"]
                              },
                              "land_use_type": {
                                  "specific": res["slu"]["name"],
                                  "generic": res["glu"]["name"]
                              },
                              } for res in similar_cases_results]
        log.debug(processed_results)
        return processed_results


    def insert_case_with_location(self, case_fields: Dict, location_fields: Dict, use_class_name: str):
        if not self.use_class_accessor.get_specific_by_name(use_class_name):
            log.error(f"Use class {use_class_name} does not exist in database.")
            raise NotImplementedError

        location_key = LocationKey(
            location_fields["block"],
            location_fields["road"],
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
