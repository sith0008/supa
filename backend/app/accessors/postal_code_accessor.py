from app.models.postal_code import PostalCode  # noqa
from typing import Dict
import logging

log = logging.getLogger('root')


class PostalCodeAccessor:
    def __init__(self, session):
        self.session = session

    def create(self, postal_code: PostalCode):
        log.info(f"Inserting postal code")
        self.session.add(postal_code)
        self.session.commit()
        log.info(f"Successfully inserted postal code")

    def read(self, filter_map: Dict):
        log.info(f"Retrieving postal code")
        log.info(filter_map)
        q = self.session.query(PostalCode)
        for k, v in filter_map.items():
            q = q.filter(getattr(PostalCode, k) == v)
        postal_codes = q.all()
        postal_codes = [g.as_dict() for g in postal_codes]
        log.info(f"Successfully retrieved postal code")
        return postal_codes

    def update(self, pri_map: Dict, upd_map: Dict):
        log.info(f"Updating postal code")
        q = self.session.query(PostalCode)
        for k, v in pri_map.items():
            q = q.filter(getattr(PostalCode, k) == v)
        q.update(upd_map)
        self.session.commit()
        log.info(f"Successfully updated postal code")

    def delete(self, pri_map: Dict):
        log.info(f"Deleting postal code")
        q = self.session.query(PostalCode)
        for k, v in pri_map.items():
            q = q.filter(getattr(PostalCode, k) == v)
        q.delete()
        self.session.commit()
        log.info(f"Successfully deleted postal code")
