from app.database import sql_db  # noqa
from sqlalchemy import (
    Column,
    VARCHAR,
    INTEGER,
    TEXT
)
from app.models.geometry import Geometry  # noqa


class ActivityGeneratingUse(sql_db.Model):
    __tablename__ = 'activity_generating_use'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    # pa_id = Column(INTEGER, primary_key=True, nullable=False)
    name = Column(VARCHAR(50), primary_key=True, nullable=False)
    subzone = Column(VARCHAR(50))
    planning_area = Column(VARCHAR(50))
    polygon = Column(TEXT)
