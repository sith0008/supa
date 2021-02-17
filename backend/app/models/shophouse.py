from app.database import sql_db  # noqa
from sqlalchemy import (
    Column,
    VARCHAR
)


# Declare Mapping
class Shophouse(sql_db.Model):
    # TODO: change fields accordingly, placeholder for testing
    __tablename__ = 'shophouse'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    block = Column(VARCHAR(20), primary_key=True)
    road = Column(VARCHAR(50), primary_key=True)
    # postal_code = Column(VARCHAR(6), primary_key=True)
    floor = Column(VARCHAR(10), primary_key=True)
    unit = Column(VARCHAR(10), primary_key=True)
    use_class = Column(VARCHAR(50), primary_key=True)
    allowed = Column(VARCHAR(1), default='N')
    reason = Column(VARCHAR(1500), default='NIL')

    # pet_shop = Column(VARCHAR(1), default='N')
    # pet_shop_reason = Column(VARCHAR(100), default='NIL')
    # residential = Column(VARCHAR(1), default='N')
    # residential_reason = Column(VARCHAR(100), default='NIL')
    # restaurant = Column(VARCHAR(1), default='N')
    # restaurant_reason = Column(VARCHAR(100), default='NIL')
    # backpackers_hostel = Column(VARCHAR(1), default='N')
    # backpackers_hostel_reason = Column(VARCHAR(100), default='NIL')
    # industrial_showroom = Column(VARCHAR(1), default='N')
    # industrial_showroom_reason = Column(VARCHAR(100), default='NIL')
    # serviced_apartment = Column(VARCHAR(1), default='N')
    # serviced_apartment_reason = Column(VARCHAR(100), default='NIL')
    # laundromat = Column(VARCHAR(1), default='N')
    # laundromat_reason = Column(VARCHAR(100), default='NIL')
    # amusement_centre = Column(VARCHAR(1), default='N')
    # amusement_centre_reason = Column(VARCHAR(100), default='NIL')
    # workers_dormitories = Column(VARCHAR(1), default='N')
    # workers_dormitories_reason = Column(VARCHAR(100), default='NIL')
    # students_hostel = Column(VARCHAR(1), default='N')
    # students_hostel_reason = Column(VARCHAR(100), default='NIL')
    # nightclub = Column(VARCHAR(1), default='N')
    # nightclub_reason = Column(VARCHAR(100), default='NIL')
    # general_industrial_use = Column(VARCHAR(1), default='N')
    # general_industrial_use_reason = Column(VARCHAR(100), default='NIL')
    # childcare_centre = Column(VARCHAR(1), default='N')
    # childcare_centre_reason = Column(VARCHAR(100), default='NIL')
    # medical_clinic = Column(VARCHAR(1), default='N')
    # medical_clinic_reason = Column(VARCHAR(100), default='NIL')
    # hotel = Column(VARCHAR(1), default='N')
    # hotel_reason = Column(VARCHAR(100), default='NIL')
    # industrial_canteen = Column(VARCHAR(1), default='N')
    # industrial_canteen_reason = Column(VARCHAR(100), default='NIL')
    # fitness_centre_gymnasium = Column(VARCHAR(1), default='N')
    # fitness_centre_gymnasium_reason = Column(VARCHAR(100), default='NIL')
    # restaurant_and_bar = Column(VARCHAR(1), default='N')
    # restaurant_and_bar_reason = Column(VARCHAR(100), default='NIL')
    # massage_establishment = Column(VARCHAR(1), default='N')
    # massage_establishment_reason = Column(VARCHAR(100), default='NIL')
    # commercial_school = Column(VARCHAR(1), default='N')
    # commercial_school_reason = Column(VARCHAR(100), default='NIL')
    # limited_and_non_exclusive_religious_use = Column(VARCHAR(1), default='N')
    # limited_and_non_exclusive_religious_use_reason = Column(VARCHAR(100), default='NIL')
    # shop = Column(VARCHAR(1), default='N')
    # shop_reason = Column(VARCHAR(100), default='NIL')
    # light_industrial_use = Column(VARCHAR(1), default='N')
    # light_industrial_use_reason = Column(VARCHAR(100), default='NIL')
    # office = Column(VARCHAR(1), default='N')
    # office_reason = Column(VARCHAR(100), default='NIL')
    # bar_pub = Column(VARCHAR(1), default='N')
    # bar_pub_reason = Column(VARCHAR(100), default='NIL')
