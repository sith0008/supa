from app.accessors.use_class_accessor import UseClassAccessor # noqa
from app.models.use_class import SpecificUseClass, GenericUseClass, SpecificUseClassEnum, GenericUseClassEnum, UseClassType, SpecificUseClassExample # noqa
from typing import Union, Dict
import logging

log = logging.getLogger('root')

class UseClassService:
    def __init__(self, graph):
        self.graph = graph
        self.accessor = UseClassAccessor(graph)

    def get(self, filter_map: Dict):
        log.debug(filter_map)
        query_type, query_param = filter_map["type"], filter_map["query"]
        if query_type == "single":
            return self.get_by_name(query_param)
        elif query_type == "multiple":
            if query_param in [el.value for el in GenericUseClassEnum]:
                return self.get_specific_by_generic(query_param)
            else:
                return self.get_all_by_type(query_param)

    def get_by_name(self, use_class_name: str):
        log.debug(f"Use class name: {use_class_name}")
        if use_class_name in [el.value for el in SpecificUseClassEnum]:
            use_class = self.accessor.get_specific_by_name(use_class_name)
        elif use_class_name in [el.value for el in GenericUseClassEnum]:
            use_class = self.accessor.get_generic_by_name(use_class_name)
        else:
            raise Exception("Invalid use class name")
        return use_class

    def get_all_by_type(self, use_class_type: str):
        log.debug(f"Use class type: {use_class_type}")
        if use_class_type == UseClassType.Specific.name:
            use_classes = self.accessor.get_all_specific()
        elif use_class_type == UseClassType.Generic.name:
            use_classes = self.accessor.get_all_generic()
        else:
            raise Exception("Invalid use class type.")
        return use_classes

    def get_specific_by_generic(self, generic_use_class_name: str):
        return self.accessor.get_specific_by_generic(generic_use_class_name)

    def get_generic_by_specific(self, specific_use_class_name: str):
        return self.accessor.get_generic_by_specific(specific_use_class_name)

    def create(self, fields_map: Dict):
        use_class_type = fields_map["type"]
        del fields_map["type"]
        if use_class_type == UseClassType.Specific.name:
            generic_use_class = fields_map["generic"]
            del fields_map["generic"]
            return self.create_specific(fields_map, generic_use_class)
        elif use_class_type == UseClassType.Generic.name:
            return self.create_generic(fields_map)
        else:
            raise Exception(f"Invalid use class type {use_class_type}")
    # calls create_generic of accessor
    def create_generic(self, fields_map: Dict):
        new_use_class = GenericUseClass()
        for k, v in fields_map.items():
            setattr(new_use_class, k, v)
        return self.accessor.create_generic(new_use_class)

    # calls create_specifc and create_is_a_relation of accessor
    def create_specific(self, fields_map: Dict, generic_use_class_name: str):
        new_use_class = SpecificUseClass()
        for k, v in fields_map.items():
            setattr(new_use_class, k, v)
        new_use_class_id = self.accessor.create_specific(new_use_class)
        relation_id = self.accessor.create_is_a_relation(new_use_class.name, generic_use_class_name)
        return new_use_class_id

    # TODO: update use class method, to be implemented after use class model is updated

    # calls delete_specific/delete_generic
    def delete(self, use_class_name: str, use_class_type: UseClassType):
        if use_class_type == UseClassType.Specific.name:
            self.accessor.delete_specific(use_class_name)
        elif use_class_type == UseClassType.Generic.name:
            self.accesor.delete_generic(use_class_name)
        else:
            raise Exception(f"Invalid use class type {use_class_type}")

    def get_specific_examples(self, filter_map:Dict):
        specific_use_class_name = filter_map["specific_use_class"]
        return self.accessor.get_specific_examples(specific_use_class_name)

    def create_specific_example(self, fields_map: Dict):
        new_use_class_example = SpecificUseClassExample()
        specific_use_class_name = fields_map["specific_use_class"]
        del fields_map["specific_use_class"]
        for k, v in fields_map.items():
            setattr(new_use_class_example, k, v)
        new_use_class_example_id = self.accessor.create_specific_example(new_use_class_example)
        relation_id = self.accessor.create_example_is_a_relation(new_use_class_example.name, specific_use_class_name)
        return new_use_class_example_id
