from app.accessors.guidelines_accessor import GuidelinesAccessor  # noqa
from app.models.guidelines import Guideline, OutcomePriority # noqa
from sqlalchemy.orm import sessionmaker
from typing import Dict
import logging

log = logging.getLogger('root')


class GuidelinesService:
    def __init__(self, engine):
        self.engine = engine

    @staticmethod
    def fill_default(fields_map):
        fields_map['unit_type'] = 'Normal' if 'unit_type' not in fields_map else fields_map['unit_type']
        fields_map['conditions'] = 'Normal' if 'conditions' not in fields_map else fields_map['conditions']
        return fields_map

    def insert_guideline(self, fields_map: Dict):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        accessor = GuidelinesAccessor(session)

        new_guideline = Guideline()
        fields_map = self.fill_default(fields_map)
        for k, v in fields_map.items():
            setattr(new_guideline, k, v)
        accessor.create(new_guideline)

        session.close()

    def get_guidelines(self, filter_map: Dict):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        accessor = GuidelinesAccessor(session)

        guidelines = accessor.read(filter_map)

        session.close()

        return guidelines

    def update_guideline(self, fields_map: Dict):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        accessor = GuidelinesAccessor(session)

        fields_map = self.fill_default(fields_map)
        pri_map = {x: fields_map[x] for x in ['business_use_type', 'property_type', 'unit_type', 'conditions']}
        upd_map = {x: fields_map[x] for x in ['outcome', 'remarks']}
        accessor.update(pri_map, upd_map)

        session.close()

    def delete_guideline(self, fields_map: Dict):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        accessor = GuidelinesAccessor(session)

        fields_map = self.fill_default(fields_map)
        pri_map = {x: fields_map[x] for x in ['business_use_type', 'property_type', 'unit_type', 'conditions']}
        accessor.delete(pri_map)

        session.close()
