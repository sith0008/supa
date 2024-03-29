from enum import Enum, EnumMeta


class GenericUseClass:
    def __init__(self, name: str = None):
        self.name = name

class SpecificUseClass:
    def __init__(self,
                 name: str = None,
                 definition: str = None,
                 requirements: str = None
                 ):
        self.name = name
        self.definition = definition
        self.requirements = requirements

class SpecificUseClassExample:
    def __init__(self,
                 name: str = None,
                 category: str = None,
                 ):
        self.name = name
        self.category = category

class UseClassType(Enum):
    Generic = "Generic"
    Specific = "Specific"

class MetaEnum(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        return True

class BaseEnum(Enum, metaclass=MetaEnum):
    pass

class GenericUseClassEnum(BaseEnum):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        return True

    FoodBev = "FoodBev"
    ShopOfficeSvc = "ShopOfficeSvc"
    Education = "Education"
    SportsRec = "SportsRec"
    Accommodation = "Accommodation"
    IndRelatedUse = "IndRelatedUse"
    CommunityRelatedUse = "CommunityRelatedUse"
    ReligiousUse = "ReligiousUse"


class SpecificUseClassEnum(BaseEnum):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        return True

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
    SpecificUseClassEnum.CommunityClub: GenericUseClassEnum.CommunityRelatedUse,
    SpecificUseClassEnum.ReligiousActivities: GenericUseClassEnum.ReligiousUse,
    SpecificUseClassEnum.LimitedReligiousUse: GenericUseClassEnum.ReligiousUse,
}
