from app.accessors.postal_code_accessor import PostalCodeAccessor  # noqa
from app.models.postal_code import PostalCode # noqa
from sqlalchemy.orm import sessionmaker
from typing import Dict
import logging

log = logging.getLogger('root')


class PostalCodeService:
    def __init__(self, engine):
        self.engine = engine
        self.pri_keys = ['block', 'road', 'postal_code']
        self.upd_keys = ['land_use_type', 'property_type']

    def insert_postal_code(self, fields_map: Dict):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        accessor = PostalCodeAccessor(session)

        new_postal_code = PostalCode()
        for k, v in fields_map.items():
            setattr(new_postal_code, k, v)
        accessor.create(new_postal_code)

        session.close()

    def get_postal_code(self, filter_map: Dict):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        accessor = PostalCodeAccessor(session)

        postal_code = accessor.read(filter_map)

        session.close()

        return postal_code

    def update_postal_code(self, fields_map: Dict):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        accessor = PostalCodeAccessor(session)

        pri_map = {x: fields_map[x] for x in self.pri_keys}
        upd_map = {x: fields_map[x] for x in self.upd_keys}
        accessor.update(pri_map, upd_map)

        session.close()

    def delete_postal_code(self, fields_map: Dict):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        accessor = PostalCodeAccessor(session)

        pri_map = {x: fields_map[x] for x in self.pri_keys}
        accessor.delete(pri_map)

        session.close()
