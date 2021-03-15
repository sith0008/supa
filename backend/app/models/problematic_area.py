from app.database import sql_db  # noqa
# from geoalchemy2 import Geometry
from sqlalchemy import (
    Column,
    VARCHAR,
    INTEGER,
    TEXT
)
from sqlalchemy import func
from sqlalchemy.types import UserDefinedType


class Geometry(UserDefinedType):
    def get_col_spec(self):
        return 'GEOMETRY'

    def bind_expression(self, bindvalue):
        return func.ST_GeomFromText(bindvalue, type_=self)

    def column_expression(self, col):
        return func.ST_AsText(col, type_=self)


class ProblematicArea(sql_db.Model):
    # TODO: change fields accordingly, placeholder for testing
    __tablename__ = 'problematic_area'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    # pa_id = Column(INTEGER, primary_key=True, nullable=False)
    name = Column(VARCHAR(50), primary_key=True, nullable=False)
    subzone = Column(VARCHAR(50))
    planning_area = Column(VARCHAR(50))
    polygon = Column(TEXT)
