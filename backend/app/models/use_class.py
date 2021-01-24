from py2neo.ogm import Model, Property, RelatedTo
from enum import Enum


class GenericUseClass(Model):
    name = Property()
    __primarykey__ = "name"


class SpecificUseClass(Model):
    name = Property()
    __primarykey__ = "name"
    is_a = RelatedTo(GenericUseClass)


class GenericUseClassEnum(Enum):
    FoodBev = "FoodBev"
    ShopOfficeSvc = "ShopOfficeSvc"
    Education = "Education"
    SportsRec = "SportsRec"
    Accommodation = "Accommodation"
    IndRelatedUse = "IndRelatedUse"
    CommunityRelatedUse = "CommunityRelatedUse"
    ReligiousUse = "ReligiousUse"


class SpecificUseClassEnum(Enum):
    # Food and Beverage
    Restaurant = "Restaurant"
    BarPub = "Bar/Pub"
    RestaurantBar = "Restaurant and Bar"
    Nightclub = "Nightclub"

    # Shop, Office and Services
    Shop = "Shop"
    Laundromat = "Laundromat"
    Office = "Office"
    MassageEstablishment = "Massage Establishment"
    MedicalClinic = "Medical Clinic"
    PetShop = "Pet Shop"
    PetBoarding = "Pet Boarding"

    # Education
    CommercialSchool = "Commercial School"
    Childcare = "Childcare Centre"

    # Sports and Recreation
    FitnessCentre = "Fitness Centre"
    AmusementCentre = "Amusement Centre"

    # Accommodation
    Residential = "Residential"
    BackpackerHostel = "Backpackers' Hostel"
    Hotel = "Hotel"
    StudentHostel = "Students' Hostel"
    ServiceApartment = "Serviced Apartment"
    WorkerDorm = "Workers' Dormitories"

    # Industrial-related uses
    LightIndUse = "Light Industrial Use"
    GeneralIndUse = "General Industrial Use"
    IndTraining = "Industrial Training"
    Warehouse = "Warehouse"
    IndCanteen = "Industrial Canteen"
    Showroom = "Showroom"
    EBusiness = "E-Business"
    CoreMediaActivities = "Core Media Activities"

    # Community-related uses
    CommunityClub = "Association/CommunityClub/Family Service Centre"

    # Religious Use
    ReligiousActivities = "Religious Activities"
    LimitedReligiousUse = "Limited & Non-Exclusive Religious Use"


use_class_map = {
    SpecificUseClassEnum.Restaurant: GenericUseClassEnum.FoodBev,
    SpecificUseClassEnum.BarPub: GenericUseClassEnum.FoodBev,
    SpecificUseClassEnum.RestaurantBar: GenericUseClassEnum.FoodBev,
    SpecificUseClassEnum.Nightclub: GenericUseClassEnum.FoodBev,
    SpecificUseClassEnum.Shop: GenericUseClassEnum.ShopOfficeSvc,
    SpecificUseClassEnum.Laundromat: GenericUseClassEnum.ShopOfficeSvc,
    SpecificUseClassEnum.Office: GenericUseClassEnum.ShopOfficeSvc,
    SpecificUseClassEnum.MassageEstablishment: GenericUseClassEnum.ShopOfficeSvc,
    SpecificUseClassEnum.MedicalClinic: GenericUseClassEnum.ShopOfficeSvc,
    SpecificUseClassEnum.PetShop: GenericUseClassEnum.ShopOfficeSvc,
    SpecificUseClassEnum.PetBoarding: GenericUseClassEnum.ShopOfficeSvc,
    SpecificUseClassEnum.CommercialSchool: GenericUseClassEnum.Education,
    SpecificUseClassEnum.Childcare: GenericUseClassEnum.Education,
    SpecificUseClassEnum.FitnessCentre: GenericUseClassEnum.SportsRec,
    SpecificUseClassEnum.AmusementCentre: GenericUseClassEnum.SportsRec,
    SpecificUseClassEnum.Residential: GenericUseClassEnum.Accommodation,
    SpecificUseClassEnum.BackpackerHostel: GenericUseClassEnum.Accommodation,
    SpecificUseClassEnum.Hotel: GenericUseClassEnum.Accommodation,
    SpecificUseClassEnum.StudentHostel: GenericUseClassEnum.Accommodation,
    SpecificUseClassEnum.ServiceApartment: GenericUseClassEnum.Accommodation,
    SpecificUseClassEnum.WorkerDorm: GenericUseClassEnum.Accommodation,
    SpecificUseClassEnum.LightIndUse: GenericUseClassEnum.IndRelatedUse,
    SpecificUseClassEnum.GeneralIndUse: GenericUseClassEnum.IndRelatedUse,
    SpecificUseClassEnum.IndTraining: GenericUseClassEnum.IndRelatedUse,
    SpecificUseClassEnum.Warehouse: GenericUseClassEnum.IndRelatedUse,
    SpecificUseClassEnum.IndCanteen: GenericUseClassEnum.IndRelatedUse,
    SpecificUseClassEnum.Showroom: GenericUseClassEnum.IndRelatedUse,
    SpecificUseClassEnum.EBusiness: GenericUseClassEnum.IndRelatedUse,
    SpecificUseClassEnum.CoreMediaActivities: GenericUseClassEnum.IndRelatedUse,
    SpecificUseClassEnum.CommunityClub: GenericUseClassEnum.CoommunityRelatedUse,
    SpecificUseClassEnum.ReligiousActivities: GenericUseClassEnum.ReligiousUse,
    SpecificUseClassEnum.LimitedReligiousUse: GenericUseClassEnum.ReligiousUse,
}
