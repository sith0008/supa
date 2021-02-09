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
    Business = "Business"
    Commercial = "Commercial"
    Residential = "Residential"
    MixedDev = "MixedDev"
    SpecialisedUse = "SpecialisedUse"


class SpecificLandUseTypeEnum(Enum):
    Residential = "Residential"
    ResComm1st = "Residential with Commercial at 1st storey"
    ResComm = "Commercial & Residential"
    ResInstitution = "Residential/Institution"
    Commercial = "Commercial"
    CommInstitution = "Commercial/Institution"
    Hotel = "Hotel"
    White = "White"
    BusinessPark = "Business Park"
    BusinessParkWhite = "Business Park - White"
    Business1 = "Business 1 (B1)"
    Business2 = "Business 2 (B2)"
    Business1White = "Business 1 - White"
    Business2White = "Business 2 - White"
    HealthMed = "Health & Medical Care"
    EduInstitution = "Educational Institution"
    PlaceOfWorship = "Place of Worship"
    CivicCommunityInstitution = "Civic & Community Institution"


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
