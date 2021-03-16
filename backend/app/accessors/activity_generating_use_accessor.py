from app.models.activity_generating_use import ActivityGeneratingUse  # noqa
from typing import Dict
import logging

log = logging.getLogger('root')


class ActivityGeneratingUseAccessor:
    def __init__(self, session):
        self.session = session

    def create(self, activity_generating_use: ActivityGeneratingUse):
        log.info(f"Inserting activity generating use")
        self.session.merge(activity_generating_use)
        self.session.commit()
        log.info(f"Successfully inserted activity generating use")

    def read(self, filter_map: Dict):
        log.info(f"Retrieving activity generating use")
        q = self.session.query(ActivityGeneratingUse)
        for k, v in filter_map.items():
            q = q.filter(getattr(ActivityGeneratingUse, k) == v)
        activity_generating_uses = q.all()
        activity_generating_uses = [g.as_dict() for g in activity_generating_uses]
        for activity_generating_use in activity_generating_uses:
            log.info(f"Successfully retrieved activity generating use" + str(activity_generating_use))
        return activity_generating_uses

    def update(self, pri_map: Dict, upd_map: Dict):
        log.info(f"Updating activity generating use")
        q = self.session.query(ActivityGeneratingUse)
        for k, v in pri_map.items():
            q = q.filter(getattr(ActivityGeneratingUse, k) == v)
        activity_generating_uses = q.all()
        activity_generating_uses = [g.as_dict() for g in activity_generating_uses]
        q.update(upd_map)
        self.session.commit()
        for activity_generating_use in activity_generating_uses:
            log.info(f"Successfully updated activity generating use" + str(activity_generating_use))

    def delete(self, pri_map: Dict):
        log.info(f"Deleting activity generating use")
        q = self.session.query(ActivityGeneratingUse)
        for k, v in pri_map.items():
            q = q.filter(getattr(ActivityGeneratingUse, k) == v)
        activity_generating_uses = q.all()
        activity_generating_uses = [g.as_dict() for g in activity_generating_uses]
        q.delete()
        self.session.commit()
        for activity_generating_use in activity_generating_uses:
            log.info(f"Successfully deleted activity generating use" + str(activity_generating_use))

    def within(self, sql_text):
        log.info(f"Checking if point lies within a activity generating use")
        results = self.session.execute(sql_text)
        for result in results:
            log.info(f"Point within activity generating use" + str(result))
            return True
        log.info(f"Point not within any activity generating use")
        return False
