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

    def get_guideline(self, filter_map: Dict):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        accessor = GuidelinesAccessor(session)
        guidelines = accessor.get_guidelines(filter_map)
        # session.commit()
        session.close()
        log.info(guidelines, type(guidelines))
        return guidelines

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

    def insert_guideline(self, fields_map: Dict):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        accessor = GuidelinesAccessor(session)
        new_guideline = Guideline()
        for k, v in fields_map.items():
            setattr(new_guideline, k, v)
        return accessor.create(new_guideline)

