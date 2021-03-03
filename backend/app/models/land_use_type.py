from enum import Enum


class GenericLandUseType:
    def __init__(self, name: str = None):
        self.name = name


class SpecificLandUseType:
    def __init__(self, name: str = None):
        self.name = name

class LandUseTypeEnum(Enum):
    Generic = "Generic"
    Specific = "Specific"

class GenericLandUseTypeEnum(Enum):
    Business = "BUSINESS"
    Commercial = "COMMERCIAL_GEN"
    Residential = "RESIDENTIAL_GEN"
    MixedDev = "MIXED_DEVELOPMENT"
    SpecialisedUse = "SPECIALISED_USE"


class SpecificLandUseTypeEnum(Enum):
    Residential = "RESIDENTIAL"
    ResComm1st = "RESIDENTIAL WITH COMMERCIAL AT 1ST STOREY"
    ResComm = "COMMERCIAL & RESIDENTIAL"
    ResInstitution = "RESIDENTIAL / INSTITUTION"
    Commercial = "COMMERCIAL"
    CommInstitution = "COMMERCIAL / INSTITUTION"
    Hotel = "HOTEL"
    White = "WHITE"
    BusinessPark = "BUSINESS PARK"
    BusinessParkWhite = "BUSINESS PARK - WHITE"
    Business1 = "BUSINESS 1"
    Business2 = "BUSINESS 2"
    Business1White = "BUSINESS 1 - WHITE"
    Business2White = "BUSINESS 2 - WHITE"
    HealthMed = "HEALTH & MEDICAL CARE"
    EduInstitution = "EDUCATIONAL INSTITUTION"
    PlaceOfWorship = "PLACE OF WORSHIP"
    CivicCommunityInstitution = "CIVIC & COMMUNITY INSTITUTION"

land_use_type_map = {
    SpecificLandUseTypeEnum.Residential: GenericLandUseTypeEnum.Residential,
    SpecificLandUseTypeEnum.ResComm1st: GenericLandUseTypeEnum.MixedDev,
    SpecificLandUseTypeEnum.ResComm: GenericLandUseTypeEnum.MixedDev,
    SpecificLandUseTypeEnum.ResInstitution: GenericLandUseTypeEnum.Residential,
    SpecificLandUseTypeEnum.Commercial: GenericLandUseTypeEnum.Commercial,
    SpecificLandUseTypeEnum.CommInstitution: GenericLandUseTypeEnum.Commercial,
    SpecificLandUseTypeEnum.Hotel: GenericLandUseTypeEnum.SpecialisedUse,
    SpecificLandUseTypeEnum.White: GenericLandUseTypeEnum.MixedDev,
    SpecificLandUseTypeEnum.BusinessPark: GenericLandUseTypeEnum.Business,
    SpecificLandUseTypeEnum.BusinessParkWhite: GenericLandUseTypeEnum.Business,
    SpecificLandUseTypeEnum.Business1: GenericLandUseTypeEnum.Business,
    SpecificLandUseTypeEnum.Business2: GenericLandUseTypeEnum.Business,
    SpecificLandUseTypeEnum.Business1White: GenericLandUseTypeEnum.Business,
    SpecificLandUseTypeEnum.Business2White: GenericLandUseTypeEnum.Business,
    SpecificLandUseTypeEnum.HealthMed: GenericLandUseTypeEnum.SpecialisedUse,
    SpecificLandUseTypeEnum.EduInstitution: GenericLandUseTypeEnum.SpecialisedUse,
    SpecificLandUseTypeEnum.PlaceOfWorship: GenericLandUseTypeEnum.SpecialisedUse,
    SpecificLandUseTypeEnum.CivicCommunityInstitution: GenericLandUseTypeEnum.SpecialisedUse,
}
