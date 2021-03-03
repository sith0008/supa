from app.models.shophouse import Shophouse  # noqa
from typing import Dict
import logging

log = logging.getLogger('root')


class ShophouseAccessor:
    def __init__(self, session):
        self.session = session

    def create(self, shophouse: Shophouse):
        log.info(f"Inserting shophouse")
        self.session.merge(shophouse)
        self.session.commit()
        log.info(f"Successfully inserted shophouse")

    def read(self, filter_map: Dict):
        log.info(f"Retrieving shophouse")
        q = self.session.query(Shophouse)
        for k, v in filter_map.items():
            q = q.filter(getattr(Shophouse, k) == v)
        shophouses = q.all()
        shophouses = [g.as_dict() for g in shophouses]
        for shophouse in shophouses:
            log.info(f"Successfully retrieved shophouse" + str(shophouse))
        return shophouses

    def update(self, pri_map: Dict, upd_map: Dict):
        log.info(f"Updating shophouse")
        q = self.session.query(Shophouse)
        for k, v in pri_map.items():
            q = q.filter(getattr(Shophouse, k) == v)
        shophouses = q.all()
        shophouses = [g.as_dict() for g in shophouses]
        q.update(upd_map)
        self.session.commit()
        for shophouse in shophouses:
            log.info(f"Successfully updated shophouse" + str(shophouse))

    def delete(self, pri_map: Dict):
        log.info(f"Deleting shophouse")
        q = self.session.query(Shophouse)
        for k, v in pri_map.items():
            q = q.filter(getattr(Shophouse, k) == v)
        shophouses = q.all()
        shophouses = [g.as_dict() for g in shophouses]
        q.delete()
        self.session.commit()
        for shophouse in shophouses:
            log.info(f"Successfully deleted shophouse" + str(shophouse))
