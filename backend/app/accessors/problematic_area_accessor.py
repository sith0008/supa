from app.models.problematic_area import ProblematicArea  # noqa
from typing import Dict
import logging

log = logging.getLogger('root')


class ProblematicAreaAccessor:
    def __init__(self, session):
        self.session = session

    def create(self, problematic_area: ProblematicArea):
        log.info(f"Inserting problematic area")
        self.session.merge(problematic_area)
        self.session.commit()
        log.info(f"Successfully inserted problematic area")

    def read(self, filter_map: Dict):
        log.info(f"Retrieving problematic area")
        q = self.session.query(ProblematicArea)
        for k, v in filter_map.items():
            q = q.filter(getattr(ProblematicArea, k) == v)
        problematic_areas = q.all()
        problematic_areas = [g.as_dict() for g in problematic_areas]
        for problematic_area in problematic_areas:
            log.info(f"Successfully retrieved problematic area" + str(problematic_area))
        return problematic_areas

    def update(self, pri_map: Dict, upd_map: Dict):
        log.info(f"Updating problematic area")
        q = self.session.query(ProblematicArea)
        for k, v in pri_map.items():
            q = q.filter(getattr(ProblematicArea, k) == v)
        problematic_areas = q.all()
        problematic_areas = [g.as_dict() for g in problematic_areas]
        q.update(upd_map)
        self.session.commit()
        for problematic_area in problematic_areas:
            log.info(f"Successfully updated problematic area" + str(problematic_area))

    def delete(self, pri_map: Dict):
        log.info(f"Deleting problematic area")
        q = self.session.query(ProblematicArea)
        for k, v in pri_map.items():
            q = q.filter(getattr(ProblematicArea, k) == v)
        problematic_areas = q.all()
        problematic_areas = [g.as_dict() for g in problematic_areas]
        q.delete()
        self.session.commit()
        for problematic_area in problematic_areas:
            log.info(f"Successfully deleted problematic area" + str(problematic_area))

    def within(self, sql_text):
        log.info(f"Checking if point lies within a problematic area")
        results = self.session.execute(sql_text)
        for result in results:
            log.info(f"Point within problematic area" + str(result))
            return True
        log.info(f"Point not within any problematic area")
        return False
