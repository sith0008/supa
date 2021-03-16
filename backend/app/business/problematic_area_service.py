from app.accessors.problematic_area_accessor import ProblematicAreaAccessor  # noqa
from app.models.problematic_area import ProblematicArea  # noqa
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from typing import Dict
import logging

log = logging.getLogger('root')


class ProblematicAreaService:
    def __init__(self, engine):
        self.engine = engine
        self.pri_keys = ['name']

    def insert_problematic_area(self, fields_map: Dict):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        accessor = ProblematicAreaAccessor(session)

        new_problematic_area = ProblematicArea()
        for k, v in fields_map.items():
            setattr(new_problematic_area, k, v)
        accessor.create(new_problematic_area)

        session.close()

    def get_problematic_area(self, filter_map: Dict):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        accessor = ProblematicAreaAccessor(session)

        problematic_area = accessor.read(filter_map)

        session.close()

        return problematic_area

    def update_problematic_area(self, fields_map: Dict):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        accessor = ProblematicAreaAccessor(session)

        pri_map = {x: fields_map[x] for x in self.pri_keys if x in fields_map}
        upd_map = {x: fields_map[x] for x in fields_map.keys() if x not in self.pri_keys}
        accessor.update(pri_map, upd_map)

        session.close()

    def delete_problematic_area(self, fields_map: Dict):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        accessor = ProblematicAreaAccessor(session)

        pri_map = {x: fields_map[x] for x in self.pri_keys if x in fields_map}
        accessor.delete(pri_map)

        session.close()

    def get_within(self, filter_map: Dict):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        accessor = ProblematicAreaAccessor(session)

        lng, lat = filter_map['lng'], filter_map['lat']

        sql_text = text(f'SELECT name FROM supa.problematic_area '
                        f'WHERE ST_CONTAINS(ST_GEOMFROMTEXT(polygon), Point({lng},{lat}))')
        within = accessor.within(sql_text)

        session.close()
        return within
