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

# Connecting
# # mysqlclient (a maintained fork of MySQL-Python)
# engine = create_engine('mysql+mysqldb://user:password@localhost/supa')
# # PyMySQL
# engine = create_engine('mysql+pymysql://scott:tiger@localhost/foo')
# engine = create_engine('sqlite:///:memory:', echo=True)
# connection = engine.connect()


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


# # Create Schema
# sql_db.Model.metadata.create_all(engine)
#
# # Create Session
# Session = sessionmaker(bind=engine)
# session = Session()
#
# # Read CSV
# with open('app/models/Guidelines_Criteria.csv') as f:
#     reader = csv.reader(f)
#     data = list(reader)
# i = 0
# for (Business_Use_Type, Property_Type, Unit_Type, Condition, Outcome, Remarks) in data:
#     Unit_Type = 'Normal' if not Unit_Type else Unit_Type
#     Conditions = 'Normal' if not Conditions else Conditions
#     guide = Guideline(
#         business_use_type=Business_Use_Type,
#         property_type=Property_Type,
#         unit_type=Unit_Type,
#         conditions=Conditions,
#         outcome=Outcome,
#         remarks=Remarks
#     )
#     # Add Object
#     session.add(guide)
#
# results = sorted(list(session.query(Guideline).filter(
#         Guideline.business_use_type == 'Restaurant and Bar',
#         Guideline.property_type == 'Commercial Buildings'
# )), key=lambda x: OutcomePriority[x.outcome])
#
# for result in results:
#     print(result)
