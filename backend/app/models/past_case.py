from py2neo.ogm import Model, Property, RelatedTo
from app.models.use_class import SpecificUseClass # noqa
from app.models.location import Location # noqa


class PastCase(Model):
    case_id = Property()
    proposed_use_desc = Property()
    gfa = Property()
    decision = Property()
    evaluation = Property()

    __primarykey__ = "case_id"

    has_use_class = RelatedTo(SpecificUseClass)
    located_in = RelatedTo(Location)