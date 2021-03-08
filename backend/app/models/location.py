# from py2neo.ogm import Model, Property, RelatedTo
from collections import namedtuple


class Location:
    def __init__(
            self,
            block: str = None,
            road: str = None,
            postal_code: int = None,
            floor: int = None,
            unit: int = None,
            building: int = None,
            lot_number: str = None,
            is_shophouse: bool = False,
    ):
        self.block = block
        self.road = road
        self.postal_code = postal_code
        self.floor = floor
        self.unit = unit
        self.building = building
        self.lot_number = lot_number
        self.is_shophouse = is_shophouse


LocationKey = namedtuple(
    "LocationKey", [
        'block',
        'road',
        'postal_code',
        'floor',
        'unit'
    ]
)
