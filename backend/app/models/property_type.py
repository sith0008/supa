from py2neo.ogm import Model, Property, RelatedTo
from enum import Enum


class GenericPropType(Model):
    name = Property()
    __primarykey__ = "name"


class SpecificPropType(Model):
    name = Property()
    __primarykey__ = "name"
    is_a = RelatedTo(GenericPropType)


class GenericPropTypeEnum(Enum):
    Business = "Business"
    Commercial = "Commercial"
    Residential = "Residential"
    MixedDev = "MixedDev"
    SpecialisedUse = "SpecialisedUse"


class SpecificPropTypeEnum(Enum):
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


prop_type_map = {
    SpecificPropTypeEnum.Residential: GenericPropTypeEnum.Residential,
    SpecificPropTypeEnum.ResComm1st: GenericPropTypeEnum.MixedDev,
    SpecificPropTypeEnum.ResComm: GenericPropTypeEnum.MixedDev,
    SpecificPropTypeEnum.ResInstitution: GenericPropTypeEnum.Residential,
    SpecificPropTypeEnum.Commercial: GenericPropTypeEnum.Commercial,
    SpecificPropTypeEnum.CommInstitution: GenericPropTypeEnum.Commercial,
    SpecificPropTypeEnum.Hotel: GenericPropTypeEnum.SpecialisedUse,
    SpecificPropTypeEnum.White: GenericPropTypeEnum.MixedDev,
    SpecificPropTypeEnum.BusinessPark: GenericPropTypeEnum.Business,
    SpecificPropTypeEnum.BusinessParkWhite: GenericPropTypeEnum.Business,
    SpecificPropTypeEnum.Business1: GenericPropTypeEnum.Business,
    SpecificPropTypeEnum.Business2: GenericPropTypeEnum.Business,
    SpecificPropTypeEnum.Business1White: GenericPropTypeEnum.Business,
    SpecificPropTypeEnum.Business2White: GenericPropTypeEnum.Business,
    SpecificPropTypeEnum.HealthMed: GenericPropTypeEnum.SpecialisedUse,
    SpecificPropTypeEnum.EduInstitution: GenericPropTypeEnum.SpecialisedUse,
    SpecificPropTypeEnum.PlaceOfWorship: GenericPropTypeEnum.SpecialisedUse,
    SpecificPropTypeEnum.CivicCommunityInstitution: GenericPropTypeEnum.SpecialisedUse,
}
