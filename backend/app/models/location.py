from py2neo.ogm import Model, Property, RelatedTo
from app.models.property_type import SpecificPropType # noqa

# TODO: add fields for PAs, PTAs, AGUs
# PA: https://www.ura.gov.sg/Corporate/Property/Business/Change-Use-of-Property-for-Business/related/Problematic-Areas
# PTA: https://www.ura.gov.sg/Corporate/Guidelines/Circulars/dc16-10#appendixa

# TODO: create new classes to represent location hierarchy (specific location -> subzone -> district -> region)

class Location(Model):
    postal_code = Property()
    building_name = Property()
    lot_number = Property()
    floor = Property()
    unit = Property()

    has_prop_type = RelatedTo(SpecificPropType)

