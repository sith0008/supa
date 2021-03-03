from app.models.guidelines import Guideline  # noqa
from typing import Dict
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

    def read(self, filter_map: Dict):
        log.info(f"Retrieving guideline")
        q = self.session.query(Guideline)
        for k, v in filter_map.items():
            q = q.filter(getattr(Guideline, k) == v)
        guidelines = q.all()
        guidelines = [g.as_dict() for g in guidelines]
        for guideline in guidelines:
            log.info(f"Successfully retrieved guideline " + str(guideline))
        return guidelines

    def update(self, pri_map: Dict, upd_map: Dict):
        log.info(f"Updating guideline")
        q = self.session.query(Guideline)
        for k, v in pri_map.items():
            q = q.filter(getattr(Guideline, k) == v)
        guidelines = q.all()
        guidelines = [g.as_dict() for g in guidelines]
        q.update(upd_map)
        self.session.commit()
        for guideline in guidelines:
            log.info(f"Successfully updated guideline " + str(guideline))

    def delete(self, pri_map: Dict):
        log.info(f"Deleting guideline")
        q = self.session.query(Guideline)
        for k, v in pri_map.items():
            q = q.filter(getattr(Guideline, k) == v)
        guidelines = q.all()
        guidelines = [g.as_dict() for g in guidelines]
        q.delete()
        self.session.commit()
        for guideline in guidelines:
            log.info(f"Successfully deleted guideline " + str(guideline))
