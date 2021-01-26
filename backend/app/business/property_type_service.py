from app.accessors.property_type_accessor import PropertyTypeAccessor # noqa
from app.models.property_type import SpecificPropType, GenericPropType, SpecificPropTypeEnum, GenericPropTypeEnum, PropTypeEnum # noqa
from typing import Union, Dict
import logging

log = logging.getLogger('root')

class PropertyTypeService:
    def __init__(self, graph):
        self.graph = graph
        self.accessor = PropertyTypeAccessor(graph)

    def get(self, filter_map: Dict):
        query_type, query_param = filter_map["type"], filter_map["query"]
        if query_type == "single":
            return self.get_by_name(query_param)
        elif query_type == "multiple":
            if query_param in GenericPropTypeEnum.__members__:
                return self.get_specific_by_generic(query_param)
            else:
                return self.get_all_by_type(query_param)

    def get_by_name(self, property_type_name: str):
        log.debug(f"Property type name: {property_type_name}")
        if property_type_name in SpecificPropTypeEnum.__members__:
            property_type = self.accessor.get_specific_by_name(property_type_name)
        elif property_type_name in GenericPropTypeEnum.__members__:
            property_type = self.accessor.get_generic_by_name(property_type_name)
        else:
            raise Exception("Invalid property type name")
        return property_type

    def get_all_by_type(self, property_type_enum: str):
        log.debug(f"Use class type: {property_type_enum}")
        if property_type_enum == PropTypeEnum.Specific.name:
            property_types = self.accessor.get_all_specific()
        elif property_type_enum == PropTypeEnum.Generic.name:
            property_types = self.accessor.get_all_generic()
        else:
            raise Exception("Invalid property type enum.")
        return property_types

    def get_specific_by_generic(self, generic_property_type_name: str):
        return self.accessor.get_specific_by_generic(generic_property_type_name)

    def create(self, fields_map: Dict):
        property_type_enum = fields_map["type"]
        del fields_map["type"]
        if property_type_enum == PropTypeEnum.Specific.name:
            generic_property_type = fields_map["generic"]
            del fields_map["generic"]
            return self.create_specific(fields_map, generic_property_type)
        elif property_type_enum == PropTypeEnum.Generic.name:
            return self.create_generic(fields_map)
        else:
            raise Exception(f"Invalid property type enum {property_type_enum}")
    # calls create_generic of accessor
    def create_generic(self, fields_map: Dict):
        new_property_type = GenericPropType()
        for k, v in fields_map.items():
            setattr(new_property_type, k, v)
        return self.accessor.create_generic(new_property_type)

    # calls create_specifc and create_is_a_relation of accessor
    def create_specific(self, fields_map: Dict, generic_property_type_name: str):
        if self.get_by_name(generic_property_type_name) is None:
            raise Exception(f"Generic property type {generic_property_type_name} does not exist")
        new_property_type = SpecificPropType()
        for k, v in fields_map.items():
            setattr(new_property_type, k, v)
        new_property_type_id = self.accessor.create_specific(new_property_type)
        relation_id = self.accessor.create_is_a_relation(new_property_type.name, generic_property_type_name)
        return new_property_type_id

    # TODO: update use class method, to be implemented after use class model is updated

    # calls delete_specific/delete_generic
    def delete(self, property_type_name: str, property_type_enum: PropTypeEnum):
        if property_type_enum == PropTypeEnum.Specific.name:
            self.accessor.delete_specific(property_type_name)
        elif property_type_enum == PropTypeEnum.Generic.name:
            self.accesor.delete_generic(property_type_name)
        else:
            raise Exception(f"Invalid property type enum {property_type_enum}")