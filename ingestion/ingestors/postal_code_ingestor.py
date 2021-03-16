import json
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    Column,
    VARCHAR
)

log = logging.getLogger('root')

supa = Flask(__name__)
supa.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://user:password@mysql-test:3306/supa'
sql_db = SQLAlchemy()
sql_db.init_app(supa)
with supa.app_context():
    engine = sql_db.engine


class PostalCode(sql_db.Model):
    __tablename__ = 'postal_code'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    block = Column(VARCHAR(20), primary_key=True)
    road = Column(VARCHAR(50), primary_key=True)
    postal_code = Column(VARCHAR(6), primary_key=True)
    land_use_type = Column(VARCHAR(50))
    property_type = Column(VARCHAR(50))
    latitude = Column(VARCHAR(50))
    longitude = Column(VARCHAR(50))


class PostalCodeIngestor:
    def __init__(self, postal_code, hdb_commercial, conserved_building, shophouse, land_use):
        self.postal_code = postal_code
        self.hdb_commercial = hdb_commercial
        self.conserved_building = conserved_building
        self.shophouse = shophouse
        self.land_use = land_use

        self.land_use_to_prop_type = {
            'COMMERCIAL': 'Commercial Buildings',
            'COMMERCIAL & RESIDENTIAL': 'Mixed Commercial & Residential Developments',
            'CIVIC & COMMUNITY INSTITUTION': 'Civic and Community Institution',
            'SPORTS & RECREATION': 'Sports & Recreation Buildings',
            'HOTEL': 'Hotel',
            'BUSINESS 1': 'Industrial Buildings',
            'BUSINESS 2': 'Industrial Buildings',
            'BUSINESS PARK': 'Business Park',
            'BUSINESS 1 - White': 'Business 1-White Buildings',
            'BUSINESS 2 - White': 'Business 2-White Buildings',
            'PLACE OF WORSHIP': 'Place of Worship',
            'EDUCATIONAL INSTITUTION': 'Educational Institution',
            'HEALTH & MEDICAL CARE': 'Medical and Healthcare',
        }

    def ingest(self):
        with open(self.postal_code) as postal_code_file:
            data_postal_code = json.load(postal_code_file)

        with open(self.hdb_commercial) as hdb_commercial_file:
            data_hdb_commercial = json.load(hdb_commercial_file)

        with open(self.conserved_building) as conserved_building_file:
            data_conserved_building = json.load(conserved_building_file)

        with open(self.shophouse) as shophouse_file:
            data_shophouse = json.load(shophouse_file)

        with open(self.land_use) as land_use_file:
            data_land_use = json.load(land_use_file)

        postal_codes = []

        for postal_code, infos in data_postal_code.items():
            seen = set()
            for info in infos:
                if (info['BLK_NO'], info['ROAD_NAME']) not in seen:
                    seen.add((info['BLK_NO'], info['ROAD_NAME']))

                    block = info['BLK_NO']
                    road = info['ROAD_NAME']
                    lat = info['LATITUDE']
                    lng = info['LONGITUDE']

                    address = block + " " + road
                    property_type = None

                    land_use_type, land_use_detail = data_land_use[postal_code]

                    # Check if hdb_commercial
                    if postal_code in data_hdb_commercial and data_hdb_commercial[postal_code] == address:
                        property_type = 'HDB Commercial Premises'

                    # Check if conserved_building
                    if postal_code in data_conserved_building:
                        property_type = 'Buildings within Historic Conservation Areas'

                    # Check if shophouse
                    elif postal_code in data_shophouse and [block, road] in data_shophouse[postal_code]:
                        property_type = 'Shophouses'

                    else:
                        # Handle conservation areas
                        if land_use_detail == 'Conservation Area':
                            property_type = 'Buildings within Historic Conservation Areas'

                        # Handle landed houses
                        elif land_use_detail and 'landed' in land_use_detail.lower():
                            property_type = 'Landed Houses'

                        # Map land use to property type
                        elif land_use_type in self.land_use_to_prop_type:
                            property_type = self.land_use_to_prop_type[land_use_type]

                    payload = {
                        'block': block, 'road': road, 'postal_code': postal_code,
                        'land_use_type': land_use_type, 'property_type': property_type,
                        'latitude': lat, 'longitude': lng
                    }
                    postal_codes.append(payload)

        conn = engine.connect()
        conn.execute(
            PostalCode.__table__.insert(),
            [
                postal_code
                for postal_code in postal_codes
            ],
        )
