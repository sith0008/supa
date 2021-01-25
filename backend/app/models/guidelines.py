from app.database import sql_db
from sqlalchemy import (
    create_engine,
    Column,
    Text,
<<<<<<< HEAD
    Integer
=======
>>>>>>> init guidelines
)
from sqlalchemy.orm import sessionmaker
import csv

<<<<<<< HEAD

class Guideline(sql_db.Model):
    # TODO: change fields accordingly, placeholder for testing
    id = Column(Integer,  primary_key=True)
    use_class = Column(Text)
=======
outcome_priority = {
    'Not Allowed': 0,
    'Unlikely': 1,
    'Submit Change Of Use Application': 2,
    'Instant Approval': 3,
    'No Planning Permission Required': 4,
}
import os
print(os.getcwd())

# Connecting
# # mysqlclient (a maintained fork of MySQL-Python)
# engine = create_engine('mysql+mysqldb://user:password@localhost/supa')
# # PyMySQL
# engine = create_engine('mysql+pymysql://scott:tiger@localhost/foo')
engine = create_engine('sqlite:///:memory:', echo=True)
# connection = engine.connect()


# Declare Mapping
class Guideline(db.Model):
    # TODO: add other fields here
    __tablename__ = 'guidelines'

    def __repr__(self):
        return "<Guideline(" \
               "Business Use Type='%s'," \
               "Property Type='%s'," \
               "Unit Type='%s'," \
               "Outcome'%s'," \
               "Remarks='%s')>" % (
                   self.business_use_type,
                   self.property_type,
                   self.unit_type,
                   self.outcome,
                   self.remarks
               )

    business_use_type = Column(Text, primary_key=True)
    property_type = Column(Text, primary_key=True)
    unit_type = Column(Text, primary_key=True)
    condition = Column(Text, primary_key=True)
    outcome = Column(Text)
    remarks = Column(Text)


# Create Schema
db.Model.metadata.create_all(engine)

# Create Session
Session = sessionmaker(bind=engine)
session = Session()

# Read CSV
with open('Guidelines_Criteria.csv') as f:
    reader = csv.reader(f)
    data = list(reader)
i = 0
for (Business_Use_Type, Property_Type, Unit_Type, Condition, Outcome, Remarks) in data:
    Unit_Type = 'Normal' if not Unit_Type else Unit_Type
    Condition = 'Normal' if not Condition else Condition
    guide = Guideline(
        business_use_type=Business_Use_Type,
        property_type=Property_Type,
        unit_type=Unit_Type,
        condition=Condition,
        outcome=Outcome,
        remarks=Remarks
    )
    # Add Object
    session.add(guide)

results = sorted(list(session.query(Guideline).filter(
        Guideline.business_use_type == 'Restaurant and Bar',
        Guideline.property_type == 'Commercial Buildings'
)), key=lambda x: outcome_priority[x.outcome])

for result in results:
    print(result)
>>>>>>> init guidelines
