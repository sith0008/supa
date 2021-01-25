from app.models.past_case import PastCase # noqa
from typing import Dict
from py2neo import Node
import logging

log = logging.getLogger('root')

class CasesAccessor:
    def __init__(self, graph):
        self.graph = graph

    def exists(self, case_id: str):
        tx = self.graph.begin()
        past_case_node_id = tx.run("MATCH (c: PastCase) WHERE c.case_id=$case_id RETURN id(c)",
                         case_id=case_id
                         ).evaluate()
        return past_case_node_id

    def get_case_by_id(self, case_id):
        if self.exists(case_id) is None:
            raise Exception(f"Case id {case_id} does not exist.")
        log.info(f"Retrieving case with case id {case_id}")
        tx = self.graph.begin()
        past_case = tx.run("MATCH (c: PastCase) WHERE c.case_id=$case_id RETURN c", case_id=case_id).evaluate()
        log.info(f"Retrieved case with case id {case_id}")
        return past_case

    # TODO: look at other "get" cases (eg. get case by decision outcome)
    # def get_cases_by_attribute(self, key, value):

    def insert(self, past_case: PastCase):
        if self.exists(past_case.case_id) is not None:
            raise Exception(f"Case id {past_case.case_id} already exists.")
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

    def update(self, past_case: PastCase):
        if self.exists(past_case.case_id) is None:
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
        if self.exists(case_id) is None:
            raise Exception(f"Case id {case_id} does not exist.")
        log.info(f"Deleting case with case id {case_id}")
        tx = self.graph.begin()
        tx.run("MATCH (c: PastCase) WHERE c.case_id=$case_id DETACH DELETE c",case_id=case_id).evaluate()
        log.info(f"Successfully deleted case with case id {case_id}")
        tx.commit()
