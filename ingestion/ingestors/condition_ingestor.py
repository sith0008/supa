import json
import logging
from shapely.geometry import shape
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    Column,
    VARCHAR,
    TEXT
)

log = logging.getLogger('root')

supa = Flask(__name__)
supa.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://user:password@mysql-test:3306/supa'
sql_db = SQLAlchemy()
sql_db.init_app(supa)
with supa.app_context():
    engine = sql_db.engine


class ProblematicTrafficArea(sql_db.Model):
    __tablename__ = 'problematic_traffic_area'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    name = Column(VARCHAR(50), primary_key=True, nullable=False)
    subzone = Column(VARCHAR(50))
    planning_area = Column(VARCHAR(50))
    polygon = Column(TEXT)


class ProblematicArea(sql_db.Model):
    __tablename__ = 'problematic_area'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    name = Column(VARCHAR(50), primary_key=True, nullable=False)
    subzone = Column(VARCHAR(50))
    planning_area = Column(VARCHAR(50))
    polygon = Column(TEXT)


class ActivityGeneratingUse(sql_db.Model):
    __tablename__ = 'activity_generating_use'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    name = Column(VARCHAR(50), primary_key=True, nullable=False)
    subzone = Column(VARCHAR(50))
    planning_area = Column(VARCHAR(50))
    polygon = Column(TEXT)


class ConditionIngestor:
    def __init__(self, problematic_area_json, problematic_traffic_area_json, activity_generating_use_json):
        self.problematic_area_json = problematic_area_json
        self.problematic_traffic_area_json = problematic_traffic_area_json
        self.activity_generating_use_json = activity_generating_use_json

    def ingest(self):

        # Problematic Traffic Areas
        with open(self.problematic_traffic_area_json) as problematic_traffic_area_file:
            data_problematic_traffic_area = json.load(problematic_traffic_area_file)

        problematic_traffic_areas = []

        for area, info in data_problematic_traffic_area.items():
            print(area)
            geom = shape(
                {
                    "coordinates": info['coords'],
                    "type": "Polygon"
                }
            )
            payload = {
                'name': area, 'subzone': info['subzone'], 'planning_area': info['planning_area'],
                'polygon': geom.wkt
            }
            problematic_traffic_areas.append(payload)

        conn = engine.connect()
        conn.execute(
            ProblematicTrafficArea.__table__.insert(),
            [
                problematic_traffic_area
                for problematic_traffic_area in problematic_traffic_areas
            ],
        )

        # Problematic Areas
        with open(self.problematic_area_json) as problematic_area_file:
            data_problematic_area = json.load(problematic_area_file)

        problematic_areas = []

        for area, info in data_problematic_area.items():
            geom = shape(
                {
                    "coordinates": info['coords'],
                    "type": "Polygon"
                }
            )
            payload = {
                'name': area, 'subzone': info['subzone'], 'planning_area': info['planning_area'],
                'polygon': geom.wkt
            }
            problematic_areas.append(payload)

        conn = engine.connect()
        conn.execute(
            ProblematicArea.__table__.insert(),
            [
                problematic_area
                for problematic_area in problematic_areas
            ],
        )

        # Activity Generating Use
        with open(self.activity_generating_use_json) as activity_generating_use_file:
            data_activity_generating_use = json.load(activity_generating_use_file)

        activity_generating_uses = []

        for area, info in data_activity_generating_use.items():
            geom = shape(
                {
                    "coordinates": info['coords'],
                    "type": "Polygon"
                }
            )
            payload = {
                'name': area, 'subzone': info['subzone'], 'planning_area': info['planning_area'],
                'polygon': geom.wkt
            }
            activity_generating_uses.append(payload)

        conn = engine.connect()
        conn.execute(
            ActivityGeneratingUse.__table__.insert(),
            [
                activity_generating_use
                for activity_generating_use in activity_generating_uses
            ],
        )
