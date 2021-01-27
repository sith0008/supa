from app.models.guidelines import Guideline  # noqa
from typing import NamedTuple, Dict
import logging

log = logging.getLogger('root')


class GuidelinesAccessor:
    def __init__(self, session):
        self.session = session

    def create(self, guideline: Guideline):
        log.info(f"Inserting guideline")
        self.session.add(guideline)
        self.session.commit()
        log.info(f"Successfully inserted guideline")
        return guideline.business_use_type, guideline.property_type, guideline.unit_type, guideline.conditions

    def read(self, filter_map: Dict):
        log.info(f"Retrieving guideline")
        q = self.session.query(Guideline)
        for k, v in filter_map.items():
            q = q.filter(getattr(Guideline, k) == v)
        guidelines = q.all()
        guidelines = [g.as_dict() for g in guidelines]
        log.info(f"Successfully retrieved guideline")
        return guidelines

    def update(self, pri_map: Dict, upd_map: Dict):
        log.info(f"Updating guideline")
        q = self.session.query(Guideline)
        for k, v in pri_map.items():
            q = q.filter(getattr(Guideline, k) == v)
        q.update(upd_map)
        self.session.commit()
        log.info(f"Successfully updated guideline")

    def delete(self, pri_map: Dict):
        log.info(f"Deleting guideline")
        q = self.session.query(Guideline)
        for k, v in pri_map.items():
            q = q.filter(getattr(Guideline, k) == v)
        q.delete()
        self.session.commit()
        log.info(f"Successfully deleted guideline")
