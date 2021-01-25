from app.accessors.cases_accessor import CasesAccessor # noqa
from app.models.past_case import PastCase # noqa
from typing import Dict


class CasesService:
    def __init__(self, graph):
        self.graph = graph
        self.accessor = CasesAccessor(graph)

    def get_case(self, filter_map: Dict):
        if "case_id" in filter_map:
            past_case = self.accessor.get_case_by_id(filter_map["case_id"])
            return past_case
        else:
            raise NotImplementedError

    def insert_case(self, fields_map: Dict):
        new_case = PastCase()
        for k, v in fields_map.items():
            setattr(new_case, k, v)
        return self.accessor.insert(new_case)

    def update_case(self, fields_map: Dict):
        new_case = PastCase()
        for k, v in fields_map.items():
            setattr(new_case, k, v)
        return self.accessor.update(new_case)

    def delete_case(self, case_id: str):
        self.accessor.delete(case_id)
