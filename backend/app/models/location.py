# from py2neo.ogm import Model, Property, RelatedTo
from app.models.property_type import SpecificPropType # noqa


class Location:
    def __init__(
            self,
            postal_code: int = None,
            floor: int = None,
            unit: int = None,
            lot_number: str = None,
            building_name: str = None
    ):
        self.postal_code = postal_code
        self.floor = floor
        self.unit = unit
        self.lot_number = lot_number
        self.building_name = building_name