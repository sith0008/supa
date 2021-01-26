# TODO: add guideline service methods here
from app.accessors.guidelines_accessor import GuidelinesAccessor  # noqa
from app.models.guidelines import Guideline, OutcomePriority # noqa
from sqlalchemy.orm import sessionmaker
from typing import Dict
import logging

log = logging.getLogger('root')


class GuidelinesService:
    def __init__(self, engine):
        self.engine = engine
        # self.accessor = GuidelinesAccessor(session)

    def insert_guideline(self, fields_map: Dict):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        accessor = GuidelinesAccessor(session)

        new_guideline = Guideline()
        for k, v in fields_map.items():
            setattr(new_guideline, k, v)
        accessor.create(new_guideline)

        session.close()

    def get_guideline(self, filter_map: Dict):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        accessor = GuidelinesAccessor(session)

        guideline = accessor.read(filter_map)

        session.close()
        return guideline

    # def get_guideline(self, filter_map: Dict):
    #     if 'business_use_type' in filter_map and 'property_type' in filter_map:
    #         if 'unit_type' in filter_map:
    #             guidelines = self.accessor.get_guidelines(
    #                 filter_map['business_use_type'],
    #                 filter_map['business_use_type'],
    #                 filter_map['unit_type'],
    #             )
    #         else:
    #             guidelines = self.accessor.get_guidelines(
    #                 filter_map['business_use_type'],
    #                 filter_map['business_use_type'],
    #             )
    #         guidelines.sort(key=lambda x: OutcomePriority[x.outcome])
    #
    #         for guideline in guidelines:
    #             if guideline.condition == 'AGU' and self.is_agu(filter_map['location']):
    #                 return guideline.outcome
    #             elif guideline.condition == 'PA' and self.is_pa(filter_map['location']):
    #                 return guideline.outcome
    #             elif guideline.condition == 'PTA' and self.is_pta(filter_map['location']):
    #                 return guideline.outcome
    #             else:
    #                 return guideline.outcome
    #         return None
    #     else:
    #         raise NotImplementedError

    def is_agu(self, location=123456):
        return True

    def is_pa(self, location=123456):
        return True

    def is_pta(self, location=123456):
        return True

    def update_guideline(self, fields_map: Dict):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        accessor = GuidelinesAccessor(session)

        fields_map['unit_type'] = 'Normal' if 'unit_type' not in fields_map else fields_map['unit_type']
        fields_map['conditions'] = 'Normal' if 'conditions' not in fields_map else fields_map['conditions']
        pri_map = {x: fields_map[x] for x in ['business_use_type', 'property_type', 'unit_type', 'conditions']}
        upd_map = {x: fields_map[x] for x in ['outcome', 'remarks']}
        accessor.update(pri_map, upd_map)

        session.close()

    def delete_guideline(self, fields_map: Dict):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        accessor = GuidelinesAccessor(session)

        fields_map['unit_type'] = 'Normal' if 'unit_type' not in fields_map else fields_map['unit_type']
        pri_map = {x: fields_map[x] for x in ['business_use_type', 'property_type', 'unit_type', 'conditions']}
        accessor.delete(pri_map)

        session.close()
