from app.models.guidelines import Guideline  # noqa
from typing import NamedTuple, Dict
import logging

log = logging.getLogger('root')


class GuidelinesAccessor:
    def __init__(self, session):
        self.session = session

    def get_guidelines(self, filter_map: Dict):
        q = self.session.query(Guideline)
        for k, v in filter_map.items():
            log.info(k, getattr(Guideline, k), v)
            # q = q.filter(getattr(Guideline, k) == v)
        guidelines = q.as_dict()
        log.info(guidelines)
        # guidelines = list(q)
        return guidelines

    def create(self, guideline: Guideline):
        log.info(f"Inserting guideline {guideline}")
        self.session.add(guideline)
        log.info(f"Successfully inserted guideline {guideline}")
        self.session.commit()
        return guideline.business_use_type, guideline.property_type, guideline.unit_type, guideline.conditions

    def read(self, guideline_key: NamedTuple):
        raise NotImplementedError

    def update(self, guideline: Guideline):
        raise NotImplementedError

    def delete(self, guideline_key: NamedTuple):
        raise NotImplementedError