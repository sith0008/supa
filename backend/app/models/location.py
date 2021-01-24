from py2neo.ogm import Model, Property, RelatedTo
from app.models.property_type import SpecificPropType # noqa


class Location(Model):
    postal_code = Property()
    building_name = Property()
    lot_number = Property()
    floor = Property()
    unit = Property()

    has_prop_type = RelatedTo(SpecificPropType)
