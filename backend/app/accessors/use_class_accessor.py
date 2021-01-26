from app.models.past_case import PastCase # noqa
from app.models.use_class import SpecificUseClass, GenericUseClass, SpecificUseClassEnum, GenericUseClassEnum # noqa
import logging

log = logging.getLogger('root')

class UseClassAccessor:
    def __init__(self, graph):
        self.graph = graph

    def get_all_generic(self):
        raise NotImplementedError

    def get_all_specific(self):
        raise NotImplementedError

    def get_specific_by_generic(self, generic_use_class: GenericUseClassEnum):
        raise NotImplementedError

    def get_generic_by_name(self, name: GenericUseClassEnum):
        raise NotImplementedError

    def get_specific_by_name(self, name: SpecificUseClassEnum):
        raise NotImplementedError

    def create_specific(self, use_class: SpecificUseClass):
        raise NotImplementedError

    def create_generic(self, use_class: GenericUseClass):
        raise NotImplementedError

    def create_is_a_relation(self, specific: SpecificUseClassEnum, generic: GenericUseClassEnum):
        raise NotImplementedError

    def update_specific(self, use_class: SpecificUseClass):
        raise NotImplementedError

    def update_generic(self, use_class: GenericUseClass):
        raise NotImplementedError

    def delete_specific(self, name: SpecificUseClassEnum):
        raise NotImplementedError

    def delete_generic(self, name: GenericUseClassEnum):
        raise NotImplementedError

