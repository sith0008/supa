from app.database import sql_db  # noqa
from sqlalchemy import (
    create_engine,
    Column,
    Text,
    Integer,
    VARCHAR
)
from sqlalchemy.orm import sessionmaker
import csv

OutcomePriority = {
    'Not Allowed': 0,
    'Unlikely': 1,
    'Submit Change Of Use Application': 2,
    'Instant Approval': 3,
    'No Planning Permission Required': 4,
}


# Declare Mapping
class Guideline(sql_db.Model):
    # TODO: change fields accordingly, placeholder for testing
    __tablename__ = 'guidelines'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    # def __repr__(self):
    #     return "<Guideline(" \
    #            "Business Use Type='%s'," \
    #            "Property Type='%s'," \
    #            "Unit Type='%s'," \
    #            "Conditions'%s'," \
    #            "Outcome'%s'," \
    #            "Remarks='%s')>" % (
    #                self.business_use_type,
    #                self.property_type,
    #                self.unit_type,
    #                self.conditions,
    #                self.outcome,
    #                self.remarks
    #            )

    business_use_type = Column(VARCHAR(100), primary_key=True)
    property_type = Column(VARCHAR(100), primary_key=True)
    unit_type = Column(VARCHAR(100), primary_key=True, default='Normal')
    conditions = Column(VARCHAR(100), primary_key=True, default='Normal')
    outcome = Column(Text)
    remarks = Column(Text, default='No Remarks')
