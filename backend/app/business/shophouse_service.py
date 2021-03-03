from app.accessors.shophouse_accessor import ShophouseAccessor  # noqa
from app.models.shophouse import Shophouse # noqa
from sqlalchemy.orm import sessionmaker
from typing import Dict
import logging

log = logging.getLogger('root')


class ShophouseService:
    def __init__(self, engine):
        self.engine = engine
        self.pri_keys = ['block', 'road', 'postal_code', 'floor', 'unit']

    def insert_shophouse(self, fields_map: Dict):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        accessor = ShophouseAccessor(session)

        new_shophouse = Shophouse()
        for k, v in fields_map.items():
            setattr(new_shophouse, k, v)
        accessor.create(new_shophouse)

        session.close()

    def get_shophouse(self, filter_map: Dict):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        accessor = ShophouseAccessor(session)

        shophouse = accessor.read(filter_map)

        ### NEED TESTING ###

        # If no exact match, remove unit
        if not shophouse:
            filter_map.pop('unit')
            shophouse = accessor.read(filter_map)

        # If still no exact match, remove floor
        if not shophouse:
            filter_map.pop('floor')
            shophouse = accessor.read(filter_map)

        session.close()

        return shophouse[0] if shophouse else []

    def update_shophouse(self, fields_map: Dict):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        accessor = ShophouseAccessor(session)

        pri_map = {x: fields_map[x] for x in self.pri_keys if x in fields_map}
        upd_map = {x: fields_map[x] for x in fields_map.keys() if x not in self.pri_keys}
        accessor.update(pri_map, upd_map)

        session.close()

    def delete_shophouse(self, fields_map: Dict):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        accessor = ShophouseAccessor(session)

        pri_map = {x: fields_map[x] for x in self.pri_keys if x in fields_map}
        accessor.delete(pri_map)

        session.close()
