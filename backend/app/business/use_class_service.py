from app.accessors.use_class_accessor import UseClassAccessor # noqa
from app.models.use_class import SpecificUseClass, GenericUseClass, SpecificUseClassEnum, GenericUseClassEnum, UseClassType # noqa
from typing import Union, Dict
import logging

log = logging.getLogger('root')

class UseClassService:
    def __init__(self, graph):
        self.graph = graph
        self.accessor = UseClassAccessor(graph)

    def get_by_name(self, use_class_name: Union[SpecificUseClassEnum, GenericUseClassEnum]):
        log.debug(f"Use class name: {use_class_name}")
        if isinstance(use_class_name, SpecificUseClassEnum):
            use_class = self.accessor.get_specific_by_name(use_class_name)
        elif isinstance(use_class_name, GenericUseClassEnum):
            use_class = self.accessor.get_generic_by_name(use_class_name)
        else:
            raise Exception("Invalid use class name")
        return use_class

    def get_all_by_type(self, use_class_type: UseClassType):
        log.debug(f"Use class type: {use_class_type}")
        if use_class_type == UseClassType.Specific:
            use_classes = self.accessor.get_all_specific()
        elif use_class_type == UseClassType.Generic:
            use_classes = self.accessor.get_all_generic()
        else:
            raise Exception("Invalid use class type.")
        return use_classes

    def get_specific_by_generic(self, generic_use_class_name: GenericUseClassEnum):
        return self.accessor.get_specific_by_generic(generic_use_class_name)

    # calls create_generic of accessor
    def create_generic(self, fields_map: Dict):
        new_use_class = GenericUseClass()
        for k, v in fields_map.items():
            setattr(new_use_class, k, v)
        return self.accessor.create_generic(new_use_class)

    # calls create_specifc and create_is_a_relation of accessor
    def create_specific(self, fields_map: Dict, generic_use_class_name: GenericUseClassEnum):
        new_use_class = SpecificUseClass()
        for k, v in fields_map.items():
            setattr(new_use_class, k, v)
        new_use_class_id = self.accessor.create_specific(new_use_class)
        relation_id = self.accessor.create_is_a_relation(new_use_class.name, generic_use_class_name)
        return new_use_class_id, relation_id

    # calls delete_specific/delete_generic
    def delete(self, name: Union[SpecificUseClassEnum, GenericUseClassEnum]):
        if isinstance(name, SpecificUseClassEnum):
            self.accessor.delete_specific(name)
        elif isinstance(name, GenericUseClassEnum):
            self.accesor.delete_generic(name)