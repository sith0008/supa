from app.models.location import Location, LocationKey # noqa
import logging
from typing import Dict

log = logging.getLogger('root')

class KnowledgeGraphChatbotService:
    def __init__(self,
                 graph,
                 sql_engine,
                 cases_service,
                 location_service,
                 use_class_service,
                 land_use_type_service,
                 guidelines_service
                 ):
        self.graph = graph
        self.engine = sql_engine
        self.cases_service = cases_service
        self.location_service = location_service
        self.use_class_service = use_class_service
        self.land_use_type_service = land_use_type_service
        self.guidelines_service = guidelines_service

    def get_similar_cases(self, params: Dict):
        try:
            specific_use_class = params["specific_use_class"]
            postal_code = params["postal_code"]
        except KeyError:
            raise Exception("Incomplete query, expected the following params: "
                            "specific_use_class and postal_code")
        log.info("Retrieving past cases similar to application")
        # get land use type from location
        specific_land_use_type = self.land_use_type_service.get_specific_by_location(postal_code)
        # get generics from specifics
        generic_land_use_type = self.land_use_type_service.get_generic_by_specific(specific_land_use_type)
        log.info(f"Address provided maps to specific land use type {specific_land_use_type} and generic land use type {generic_land_use_type}")
        generic_use_class = self.use_class_service.get_generic_by_specific(specific_use_class)
        log.info(f"Specific use class provided maps to generic use class {generic_use_class}")
        # get similar cases
        exact_similar_cases_result = self.cases_service.get_similar_case_exact(specific_use_class, specific_land_use_type)
        log.info(f"Retrieved similar cases with use class {specific_use_class} and land use type {specific_land_use_type}")
        log.debug(exact_similar_cases_result)
        extended_similar_cases_result = self.cases_service.get_similar_case_extended(specific_use_class, generic_use_class, specific_land_use_type, generic_land_use_type)
        if not exact_similar_cases_result:
            return extended_similar_cases_result
        elif not extended_similar_cases_result:
            return exact_similar_cases_result
        else:
            return exact_similar_cases_result + extended_similar_cases_result

    def generate_use_class_clarifications(self, specific_use_class_name: str):
        use_class = self.use_class_service.get_by_name(specific_use_class_name)
        # retrieve clarifications from use class
        raise NotImplementedError

    '''
    TODO: to review this method, to consider the following:
    1. unit type. is it a user input? 
    2. condition. get lat, lng from location node and do point in polygon for AGU, PTA, PA
    
    For now, we return all guidelines for the use_class and property_type given
    '''
    def get_submission_classification(self,
                                      use_class: str,
                                      block: str,
                                      road: str,
                                      postal_code: str,
                                      floor: int,
                                      unit: int
                                      ):
        land_use_type = self.land_use_type_service.get_specific_by_location(postal_code)
        location = self.location_service.get_location({
            "block": block,
            "road": road,
            "postal_code": postal_code,
            "floor": floor,
            "unit": unit
        })
        guidelines = self.guidelines_service.get_guidelines({
            "business_use_type": use_class,
            "property_type": land_use_type,
        })
        return guidelines

    # conversation caching: insert conversation
    def submit_proposal(self):
        raise NotImplementedError