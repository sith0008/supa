from app.models.property_type import PropertyType  # noqa
from typing import Dict
import logging

log = logging.getLogger('root')


class PropertyTypeAccessor:
    def __init__(self, session):
        self.session = session

    def create(self, property_type: PropertyType):
        log.info(f"Inserting property type")
        self.session.add(property_type)
        self.session.commit()
        log.info(f"Successfully inserted property type")

    def read(self, filter_map: Dict):
        log.info(f"Retrieving property type")
        q = self.session.query(PropertyType)
        for k, v in filter_map.items():
            q = q.filter(getattr(PropertyType, k) == v)
        property_types = q.all()
        property_types = [g.as_dict() for g in property_types]
        log.info(f"Successfully retrieved property type")
        return property_types

    def update(self, pri_map: Dict, upd_map: Dict):
        log.info(f"Updating property type")
        q = self.session.query(PropertyType)
        for k, v in pri_map.items():
            q = q.filter(getattr(PropertyType, k) == v)
        q.update(upd_map)
        self.session.commit()
        log.info(f"Successfully updated property type")

    def delete(self, pri_map: Dict):
        log.info(f"Deleting property type")
        q = self.session.query(PropertyType)
        for k, v in pri_map.items():
            q = q.filter(getattr(PropertyType, k) == v)
        q.delete()
        self.session.commit()
        log.info(f"Successfully deleted property type")
