from app.models.location import Location, LocationKey # noqa
import logging

log = logging.getLogger('root')

class KnowledgeGraphChatbotService:
    def __init__(self,
                 graph,
                 sql_engine,
                 cases_service,
                 location_service,
                 use_class_service,
                 property_type_service,
                 guidelines_service
                 ):
        self.graph = graph
        self.engine = sql_engine
        self.cases_service = cases_service
        self.location_service = location_service
        self.use_class_service = use_class_service
        self.property_type_service = property_type_service
        self.guidelines_service = guidelines_service

    def get_similar_cases(self,
                          specific_use_class: str,
                          postal_code: int,
                          floor: int,
                          unit: int
                          ):
        tx = self.graph.begin()
        # get prop type from location
        location_key = LocationKey(postal_code, floor, unit)
        specific_property_type = self.property_type_service.get_specific_by_location(location_key)
        # get generics from specifics
        generic_property_type = self.property_type_service.get_generic_by_specific(specific_property_type)
        generic_use_class = self.use_class_service.get_generic_by_specific(specific_use_class)
        # get similar cases
        exact_similar_cases_result = self.cases_service.get_similar_case_exact(specific_use_class, specific_property_type)
        extended_similar_cases_result = self.cases_service.get_similar_case_extended(specific_use_class, generic_use_class, specific_property_type, generic_property_type)
        similar_cases_result = exact_similar_cases_result + extended_similar_cases_result
        return similar_cases_result

    def generate_use_class_clarifications(self, specific_use_class_name: str):
        use_class = self.use_class_service.get_by_name(specific_use_class_name)
        # retrieve clarifications from use class
        raise NotImplementedError

    def get_submission_classification(self,
                                      use_class: str,
                                      postal_code: int,
                                      floor: int,
                                      unit: int
                                      ):
        location_key = LocationKey(postal_code, floor, unit)
        # get property type
        property_type = self.property_type_service.get_specific_by_location(location_key)
        # get unit type (NOT IMPLEMENTED)
        unit_type = self.location_service.get_unit_type(postal_code, floor, unit)
        # get condition type (NOT IMPLEMENTED)
        condition = self.location_service.get_condition(postal_code)
        # query mysql DB
        guidelines = self.guidelines_service.get_guidelines({
            "business_use_type": use_class,
            "property_type": property_type,
            "unit_type": unit_type,
            "conditions": condition
        })
        return guidelines

    # conversation caching: insert conversation
    def submit_proposal(self):
        raise NotImplementedError