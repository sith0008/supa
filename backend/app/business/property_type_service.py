from app.accessors.property_type_accessor import PropertyTypeAccessor  # noqa
from app.models.property_type import PropertyType # noqa
from sqlalchemy.orm import sessionmaker
from typing import Dict
import logging

log = logging.getLogger('root')


class PropertyTypeService:
    def __init__(self, engine):
        self.engine = engine

    def insert_property_type(self, fields_map: Dict):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        accessor = PropertyTypeAccessor(session)

        new_property_type = PropertyType()
        for k, v in fields_map.items():
            setattr(new_property_type, k, v)
        accessor.create(new_property_type)

        session.close()

    def get_property_type(self, filter_map: Dict):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        accessor = PropertyTypeAccessor(session)

        property_type = accessor.read(filter_map)

        session.close()

        return property_type

    def update_property_type(self, fields_map: Dict):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        accessor = PropertyTypeAccessor(session)

        pri_map = {x: fields_map[x] for x in ['block', 'road', 'postal_code']}
        upd_map = {x: fields_map[x] for x in ['property_type']}
        accessor.update(pri_map, upd_map)

        session.close()

    def delete_property_type(self, fields_map: Dict):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        accessor = PropertyTypeAccessor(session)

        pri_map = {x: fields_map[x] for x in ['block', 'road', 'postal_code']}
        accessor.delete(pri_map)

        session.close()
