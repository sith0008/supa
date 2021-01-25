from py2neo.ogm import Model, Property, RelatedTo
from app.models.use_class import SpecificUseClass # noqa
from app.models.location import Location # noqa

class PastCase:
    def __init__(
            self,
            case_id: str = None,
            proposed_use_desc: str = None,
            gfa: float = None,
            decision: str = None,
            evaluation: str = None
    ):
        self.case_id = case_id
        self.proposed_use_desc = proposed_use_desc
        self.gfa = gfa
        self.decision = decision
        self.evaluation = evaluation
