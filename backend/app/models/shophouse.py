from app.database import sql_db  # noqa
from sqlalchemy import (
    Column,
    VARCHAR
)


# Declare Mapping
class Shophouse(sql_db.Model):
    # TODO: change fields accordingly, placeholder for testing
    __tablename__ = 'shophouse'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    block = Column(VARCHAR(20), primary_key=True)
    road = Column(VARCHAR(50), primary_key=True)
    # postal_code = Column(VARCHAR(6), primary_key=True)
    floor = Column(VARCHAR(10), primary_key=True)
    unit = Column(VARCHAR(10), primary_key=True)
    use_class = Column(VARCHAR(50), primary_key=True)
    allowed = Column(VARCHAR(1), default='N')
    reason = Column(VARCHAR(1500), default='NIL')

