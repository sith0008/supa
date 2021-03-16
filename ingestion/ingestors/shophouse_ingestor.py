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


class Shophouse(sql_db.Model):
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


class ShophouseIngestor:
    def __init__(self, shophouse):
        self.shophouse = shophouse

    def ingest(self):
        with open(self.shophouse) as shophouse_file:
            data_shophouse = json.load(shophouse_file)

        shophouses = []

        for address, info in data_shophouse.items():
            block, road = address.split(' ', maxsplit=1)
            seen = set()
            for storey in info['StoreyList']:
                if ',' not in storey['storey']:  # ignore those with comma for now
                    floor, unit = (storey['storey'].split('-', maxsplit=1) + ['0'])[:2]

                    # # Clean data: floor
                    # Convert cardinal numbers to numbers
                    floor = floor.replace('1ST', '1').replace('2ND', '2').replace('3RD', '3')
                    # Remove hash symbol
                    floor = floor.replace('#', '')
                    # Strip leading 0s
                    floor = floor.lstrip('0')
                    # Default floor to '0' if None
                    if not floor: floor = '0'

                    # # Clean data: unit
                    # Strip leading 0s
                    unit = unit.lstrip('0')
                    # Default floor to '0' if None (ignore mezz unit for now)
                    if not unit or unit == 'N.A.' or unit == 'MEZZ': unit = '0'

                    for allowable in storey['allowableUseList']:
                        if 'allowed' in allowable:
                            use_class = allowable['useTypeDescr']
                            allowed = allowable['allowed']
                            reason = allowable['allowedReason']

                            if (floor, unit, use_class) not in seen:
                                seen.add((floor, unit, use_class))

                                payload = {
                                    'block': block, 'road': road, 'floor': floor, 'unit': unit,
                                    'use_class': use_class, 'allowed': allowed, 'reason': reason
                                }
                                shophouses.append(payload)

        conn = engine.connect()
        conn.execute(
            Shophouse.__table__.insert(),
            [
                shophouse
                for shophouse in shophouses
            ],
        )
