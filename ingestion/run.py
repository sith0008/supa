import os
import logging
from commons.custom_logging import CustomHandler  # noqa

from ingestors.land_use_type_ingestor import LandUseTypeIngestor  # noqa
from ingestors.use_class_ingestor import UseClassIngestor  # noqa
from ingestors.past_case_ingestor import PastCaseIngestor  # noqa
from ingestors.entity_pop_ingestor import EntityPopIngestor  # noqa
from ingestors.guidelines_ingestor import GuidelinesIngestor  # noqa
from ingestors.property_type_ingestor import PropertyTypeIngestor  # noqa
from ingestors.ura_data_ingestor import URADataIngestor  # noqa
from ingestors.location_ingestor import LocationIngestor  # noqa

log = logging.getLogger('root')
log.setLevel('DEBUG')
log.addHandler(CustomHandler())

BACKEND_HOST = os.environ.get("BACKEND_HOST", "backend:5000")

# prop_type_ingestor = PropertyTypeIngestor(BACKEND_HOST, "/proptype")  # Need to convert to land use
use_class_ingestor = UseClassIngestor(BACKEND_HOST, "/useclass")
past_case_ingestor = PastCaseIngestor(BACKEND_HOST, "/case")
location_ingestor = LocationIngestor(BACKEND_HOST, "/location")
ura_data_ingestor = URADataIngestor(past_case_ingestor, location_ingestor)
entity_pop_ingestor = EntityPopIngestor(BACKEND_HOST, "/entitypop")
guidelines_ingestor = GuidelinesIngestor(BACKEND_HOST, "/guideline")
property_type_ingestor = PropertyTypeIngestor(BACKEND_HOST, "/property_type")


def init_use_class():
    log.info("Initialising generic use classes")
    use_class_ingestor.insert_generic()
    log.info("Initialising specific use classes")
    use_class_ingestor.insert_specific()


# def init_prop_type():
#     log.info("Initialising generic property type")
#     prop_type_ingestor.insert_generic()
#     log.info("Initialising specific property type")
#     prop_type_ingestor.insert_specific()


def init_past_cases(cases_directory):
    log.info("Initialising past cases")
    ura_data_ingestor.ingest_all(cases_directory)


def main():
    GUIDELINES_CSV_FILE = os.environ.get("GUIDELINES_CSV_FILE")
    CASES_DATA_DIRECTORY = os.environ.get("INPUT_DATA_DIR")
    if os.environ.get("INIT_SQL", "true").lower() == "true":
        log.info("initialising guidelines database")
        guidelines_ingestor.ingest(GUIDELINES_CSV_FILE)

    if os.environ.get("INIT_GRAPH", "true").lower() == "true":
        # TODO: call methdos from prop_type_ingestor, use_class_ingestor, past_case_ingestor, entity_pop_ingestor
        log.info("initialising graph database")
        init_use_class()
        # init_prop_type()
        init_past_cases(CASES_DATA_DIRECTORY)


if __name__ == "__main__":
    log.info("starting ingestion")
    main()
