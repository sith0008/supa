from app.database import sql_db  # noqa
from sqlalchemy import (
    Column,
    VARCHAR
)


class PostalCode(sql_db.Model):
    # TODO: change fields accordingly, placeholder for testing
    __tablename__ = 'postal_code'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    block = Column(VARCHAR(20), primary_key=True)
    road = Column(VARCHAR(50), primary_key=True)
    postal_code = Column(VARCHAR(6), primary_key=True)
    land_use_type = Column(VARCHAR(50))
    property_type = Column(VARCHAR(50))
