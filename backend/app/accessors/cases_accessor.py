from app.models.past_case import PastCase # noqa
from app.models.location import LocationKey # noqa
import logging

log = logging.getLogger('root')

class CasesAccessor:
    def __init__(self, graph):
        self.graph = graph

    def get_case_by_id(self, case_id):
        log.info(f"Retrieving case with case id {case_id}")
        tx = self.graph.begin()
        past_case = tx.run("MATCH (c: PastCase) WHERE c.case_id=$case_id RETURN c", case_id=case_id).evaluate()
        if past_case is None:
            log.warning(f"Past case {case_id} does not exist")
        else:
            log.info(f"Retrieved case with case id {case_id}")
        tx.commit()
        return past_case

    # TODO: look at other "get" cases (eg. get case by decision outcome)
    # def get_cases_by_attribute(self, key, value):

    def insert(self, past_case: PastCase):
        log.info(f"Inserting case with case id {past_case.case_id}")
        log.debug(f"Past case fields: {past_case}")
        tx = self.graph.begin()
        insert_case_id = tx.run("CREATE (c: PastCase) SET c.case_id=$case_id, c.proposed_use_desc=$proposed_use_desc, c.gfa=$gfa, c.decision=$decision, c.evaluation=$evaluation RETURN id(c)",
               case_id=past_case.case_id,
               proposed_use_desc=past_case.proposed_use_desc,
               gfa=past_case.gfa,
               decision=past_case.decision,
               evaluation=past_case.evaluation
               ).evaluate()
        tx.commit()
        log.info(f"Successfully inserted case with case id {past_case.case_id}")
        return insert_case_id

    def insert_has_use_class_relation(self, case_id: str, use_class_name: str):
        if self.get_case_by_id(case_id) is None:
            raise Exception(f"Case id {case_id} does not exist.")
        log.info(f"Inserting HAS_USE_CLASS relation for case with case id {case_id} and use class {use_class_name}")
        tx = self.graph.begin()
        insert_has_use_class_relation_id = tx.run("MATCH (c: PastCase), (u: SpecificUseClass) "
                                                  "WHERE c.case_id=$case_id AND u.name=$name "
                                                  "CREATE (c)-[r: HAS_USE_CLASS]->(u) "
                                                  "RETURN id(r)",
                                                  case_id=case_id,
                                                  name=use_class_name).evaluate()

        tx.commit()

        log.info(f"Successfully inserted HAS_USE_CLASS relation for case {case_id} and use class {use_class_name}")
        return insert_has_use_class_relation_id

    def insert_located_in_relation(self, case_id: str, location_key: LocationKey):
        if self.get_case_by_id(case_id) is None:
            raise Exception(f"Case id {case_id} does not exist.")
        log.info(f"Inserting LOCATED_IN relation for case with case id {case_id} and location {location_key}")
        tx = self.graph.begin()
        insert_located_in_relation_id = tx.run("MATCH (c: PastCase), (l: Location) "
                                                "WHERE c.case_id=$case_id AND l.postal_code=$postal_code AND l.floor=$floor AND l.unit=$unit "
                                                "CREATE (c)-[r: LOCATED_IN]->(l) "
                                                "RETURN id(r)",
                                               case_id=case_id,
                                               postal_code=location_key.postal_code,
                                               floor=location_key.floor,
                                               unit=location_key.unit).evaluate()

        tx.commit()
        log.info(f"Successfully inserted LOCATED_IN relation for case {case_id} and use class {location_key}")
        return insert_located_in_relation_id

    def update(self, past_case: PastCase):
        if self.get_case_by_id(past_case.case_id) is None:
            raise Exception(f"Case id {past_case.case_id} does not exist.")
        log.info(f"Updating case with case id {past_case.case_id}")
        log.debug(f"Past case fields: {past_case}")
        tx = self.graph.begin()
        update_case_id = tx.run("MATCH (c: PastCase) WHERE c.case_id=$case_id SET c.proposed_use_desc=$proposed_use_desc, c.gfa=$gfa, c.decision=$decision, c.evaluation=$evaluation RETURN id(c)",
                                case_id=past_case.case_id,
                                proposed_use_desc=past_case.proposed_use_desc,
                                gfa=past_case.gfa,
                                decision=past_case.decision,
                                evaluation=past_case.evaluation
                                ).evaluate()
        tx.commit()
        log.info(f"Successfully updated case with case id {past_case.case_id}")
        return update_case_id

    def delete(self, case_id: str):
        if self.get_case_by_id(case_id) is None:
            raise Exception(f"Case id {case_id} does not exist.")
        log.info(f"Deleting case with case id {case_id}")
        tx = self.graph.begin()
        tx.run("MATCH (c: PastCase) WHERE c.case_id=$case_id DETACH DELETE c",case_id=case_id).evaluate()
        log.info(f"Successfully deleted case with case id {case_id}")
        tx.commit()
