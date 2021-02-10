from app.accessors.land_use_type_accessor import LandUseTypeAccessor # noqa
from app.models.land_use_type import SpecificLandUseType, GenericLandUseType, SpecificLandUseTypeEnum, GenericLandUseTypeEnum, LandUseTypeEnum # noqa
from app.models.location import LocationKey # noqa
from typing import Union, Dict
import logging

log = logging.getLogger('root')

class LandUseTypeService:
    def __init__(self, graph):
        self.graph = graph
        self.accessor = LandUseTypeAccessor(graph)

    def get(self, filter_map: Dict):
        query_type, query_param = filter_map["type"], filter_map["query"]
        if query_type == "single":
            return self.get_by_name(query_param)
        elif query_type == "multiple":
            if query_param in GenericLandUseTypeEnum.__members__:
                return self.get_specific_by_generic(query_param)
            else:
                return self.get_all_by_type(query_param)

    def get_by_name(self, land_use_type_name: str):
        log.debug(f"Land use type name: {land_use_type_name}")
        if land_use_type_name in SpecificLandUseTypeEnum.__members__:
            land_use_type = self.accessor.get_specific_by_name(land_use_type_name)
        elif land_use_type_name in GenericLandUseTypeEnum.__members__:
            land_use_type = self.accessor.get_generic_by_name(land_use_type_name)
        else:
            raise Exception("Invalid land use type name")
        return land_use_type

    def get_all_by_type(self, land_use_type_enum: str):
        log.debug(f"Use class type: {land_use_type_enum}")
        if land_use_type_enum == LandUseTypeEnum.Specific.name:
            land_use_types = self.accessor.get_all_specific()
        elif land_use_type_enum == LandUseTypeEnum.Generic.name:
            land_use_types = self.accessor.get_all_generic()
        else:
            raise Exception("Invalid land use type name.")
        return land_use_types

    def get_specific_by_generic(self, generic_land_use_type_name: str):
        return self.accessor.get_specific_by_generic(generic_land_use_type_name)

    def get_generic_by_specific(self, specific_land_use_type_name: str):
        return self.accessor.get_generic_by_specific(specific_land_use_type_name)

    def get_specific_by_location(self, postal_code: str):
        return self.accessor.get_specific_by_location(postal_code)

    def create(self, fields_map: Dict):
        land_use_type_enum = fields_map["type"]
        del fields_map["type"]
        if land_use_type_enum == LandUseTypeEnum.Specific.name:
            generic_land_use_type = fields_map["generic"]
            del fields_map["generic"]
            return self.create_specific(fields_map, generic_land_use_type)
        elif land_use_type_enum == LandUseTypeEnum.Generic.name:
            return self.create_generic(fields_map)
        else:
            raise Exception(f"Invalid land use type name {land_use_type_enum}")
    # calls create_generic of accessor
    def create_generic(self, fields_map: Dict):
        new_land_use_type = GenericLandUseType()
        for k, v in fields_map.items():
            setattr(new_land_use_type, k, v)
        return self.accessor.create_generic(new_land_use_type)

    # calls create_specifc and create_is_a_relation of accessor
    def create_specific(self, fields_map: Dict, generic_land_use_type_name: str):
        if self.get_by_name(generic_land_use_type_name) is None:
            raise Exception(f"Generic land use type {generic_land_use_type_name} does not exist")
        new_land_use_type = SpecificLandUseType()
        for k, v in fields_map.items():
            setattr(new_land_use_type, k, v)
        new_land_use_type_id = self.accessor.create_specific(new_land_use_type)
        relation_id = self.accessor.create_is_a_relation(new_land_use_type.name, generic_land_use_type_name)
        return new_land_use_type_id

    # TODO: update use class method, to be implemented after use class model is updated

    # calls delete_specific/delete_generic
    def delete(self, land_use_type_name: str, land_use_type_enum: LandUseTypeEnum):
        if land_use_type_enum == LandUseTypeEnum.Specific.name:
            self.accessor.delete_specific(land_use_type_name)
        elif land_use_type_enum == LandUseTypeEnum.Generic.name:
            self.accesor.delete_generic(land_use_type_name)
        else:
            raise Exception(f"Invalid land use type name {land_use_type_enum}")