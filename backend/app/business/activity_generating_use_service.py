from app.accessors.activity_generating_use_accessor import ActivityGeneratingUseAccessor  # noqa
from app.models.activity_generating_use import ActivityGeneratingUse  # noqa
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from typing import Dict
import logging

log = logging.getLogger('root')


class ActivityGeneratingUseService:
    def __init__(self, engine):
        self.engine = engine
        self.pri_keys = ['name']

    def insert_activity_generating_use(self, fields_map: Dict):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        accessor = ActivityGeneratingUseAccessor(session)

        new_activity_generating_use = ActivityGeneratingUse()
        for k, v in fields_map.items():
            setattr(new_activity_generating_use, k, v)
        accessor.create(new_activity_generating_use)

        session.close()

    def get_activity_generating_use(self, filter_map: Dict):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        accessor = ActivityGeneratingUseAccessor(session)

        activity_generating_use = accessor.read(filter_map)

        session.close()

        return activity_generating_use

    def update_activity_generating_use(self, fields_map: Dict):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        accessor = ActivityGeneratingUseAccessor(session)

        pri_map = {x: fields_map[x] for x in self.pri_keys if x in fields_map}
        upd_map = {x: fields_map[x] for x in fields_map.keys() if x not in self.pri_keys}
        accessor.update(pri_map, upd_map)

        session.close()

    def delete_activity_generating_use(self, fields_map: Dict):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        accessor = ActivityGeneratingUseAccessor(session)

        pri_map = {x: fields_map[x] for x in self.pri_keys if x in fields_map}
        accessor.delete(pri_map)

        session.close()

    def get_within(self, filter_map: Dict):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        accessor = ActivityGeneratingUseAccessor(session)

        lng, lat = filter_map['lng'], filter_map['lat']

        sql_text = text(f'SELECT name FROM supa.activity_generating_use '
                        f'WHERE ST_CONTAINS(ST_GEOMFROMTEXT(polygon), Point({lng},{lat}))')
        within = accessor.within(sql_text)

        session.close()
        return within
