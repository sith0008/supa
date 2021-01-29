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
            log.error(f"Location {location_key} does not exist in database. Creating now")
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
