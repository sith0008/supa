from app.database import sql_db  # noqa
from sqlalchemy import (
    Column,
    Text,
    VARCHAR
)

OutcomePriority = {
    'Not Allowed': 0,
    'Unlikely': 1,
    'Submit Change Of Use Application': 2,
    'Instant Approval': 3,
    'No Planning Permission Required': 4,
}


class Guideline(sql_db.Model):
    __tablename__ = 'guidelines'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    business_use_type = Column(VARCHAR(100), primary_key=True)
    property_type = Column(VARCHAR(100), primary_key=True)
    unit_type = Column(VARCHAR(100), primary_key=True, default='Normal')
    conditions = Column(VARCHAR(100), primary_key=True, default='Normal')
    outcome = Column(VARCHAR(50))
    remarks = Column(Text, default='No Remarks')
