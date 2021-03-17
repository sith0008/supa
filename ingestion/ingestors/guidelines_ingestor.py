import csv
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    Column,
    Text,
    VARCHAR
)

log = logging.getLogger('root')

supa = Flask(__name__)
supa.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://user:password@mysql-test:3306/supa'
sql_db = SQLAlchemy()
sql_db.init_app(supa)
with supa.app_context():
    engine = sql_db.engine


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


class GuidelinesIngestor:
    def __init__(self, guidelines_csv):
        self.guidelines_csv = guidelines_csv

    def ingest(self):
        csv_data = csv.reader(open(self.guidelines_csv))
        title = list(map(str.lower, next(csv_data)))

        conn = engine.connect()
        conn.execute(
            Guideline.__table__.insert(),
            [
                dict(
                    zip(title, row)
                )
                for row in csv_data
            ],
        )

