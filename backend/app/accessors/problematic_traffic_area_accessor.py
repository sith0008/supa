from app.models.problematic_traffic_area import ProblematicTrafficArea  # noqa
from typing import Dict
import logging

log = logging.getLogger('root')


class ProblematicTrafficAreaAccessor:
    def __init__(self, session):
        self.session = session

    def create(self, problematic_traffic_area: ProblematicTrafficArea):
        log.info(f"Inserting problematic traffic area")
        self.session.merge(problematic_traffic_area)
        self.session.commit()
        log.info(f"Successfully inserted problematic traffic area")

    def read(self, filter_map: Dict):
        log.info(f"Retrieving problematic traffic area")
        q = self.session.query(ProblematicTrafficArea)
        for k, v in filter_map.items():
            q = q.filter(getattr(ProblematicTrafficArea, k) == v)
        problematic_traffic_areas = q.all()
        problematic_traffic_areas = [g.as_dict() for g in problematic_traffic_areas]
        for problematic_traffic_area in problematic_traffic_areas:
            log.info(f"Successfully retrieved problematic traffic area" + str(problematic_traffic_area))
        return problematic_traffic_areas

    def update(self, pri_map: Dict, upd_map: Dict):
        log.info(f"Updating problematic traffic area")
        q = self.session.query(ProblematicTrafficArea)
        for k, v in pri_map.items():
            q = q.filter(getattr(ProblematicTrafficArea, k) == v)
        problematic_traffic_areas = q.all()
        problematic_traffic_areas = [g.as_dict() for g in problematic_traffic_areas]
        q.update(upd_map)
        self.session.commit()
        for problematic_traffic_area in problematic_traffic_areas:
            log.info(f"Successfully updated problematic traffic area" + str(problematic_traffic_area))

    def delete(self, pri_map: Dict):
        log.info(f"Deleting problematic traffic area")
        q = self.session.query(ProblematicTrafficArea)
        for k, v in pri_map.items():
            q = q.filter(getattr(ProblematicTrafficArea, k) == v)
        problematic_traffic_areas = q.all()
        problematic_traffic_areas = [g.as_dict() for g in problematic_traffic_areas]
        q.delete()
        self.session.commit()
        for problematic_traffic_area in problematic_traffic_areas:
            log.info(f"Successfully deleted problematic traffic area" + str(problematic_traffic_area))

    def within(self, sql_text):
        log.info(f"Checking if point lies within a problematic traffic area")
        results = self.session.execute(sql_text)
        for result in results:
            log.info(f"Point within problematic traffic area" + str(result))
            return True
        log.info(f"Point not within any problematic traffic area")
        return False
