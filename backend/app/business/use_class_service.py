from app.accessors.use_class_accessor import UseClassAccessor # noqa
from app.models.use_class import SpecificUseClass, GenericUseClass, SpecificUseClassEnum, GenericUseClassEnum # noqa
from typing import Union

class UseClassService:
    def __init__(self, graph):
        self.graph = graph
    # general get method, take in argument to know which accessor method to call
    def get(self, filter_type: Union[SpecificUseClassEnum, GenericUseClassEnum, str]):
        raise NotImplementedError
    # calls create_generic of accessor
    def create_generic(self):
        raise NotImplementedError
    # calls create_specifc and create_is_a_relation of accessor
    def create_specific(self):
        raise NotImplementedError
    # calls delete_specific/delete_generic
    def delete(self, name: Union[SpecificUseClassEnum, GenericUseClassEnum]):
        raise NotImplementedError
