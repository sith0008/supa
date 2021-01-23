from backend.app.models.guidelines import Guideline
from typing import NamedTuple

class GuidelinesAccessor:
    def __init__(self, session):
        self.session = session

    def create(self, guideline: Guideline):
        raise NotImplementedError

    def read(self, guideline_key: NamedTuple):
        raise NotImplementedError

    def update(self, guideline: Guideline):
        raise NotImplementedError

    def delete(self, guideline_key: NamedTuple):
        raise NotImplementedError