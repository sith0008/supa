import os
import logging
from commons.custom_logging import CustomHandler  # noqa

from ingestors.land_use_type_ingestor import LandUseTypeIngestor  # noqa
from ingestors.use_class_ingestor import UseClassIngestor  # noqa
from ingestors.past_case_ingestor import PastCaseIngestor  # noqa
from ingestors.entity_pop_ingestor import EntityPopIngestor  # noqa
from ingestors.guidelines_ingestor import GuidelinesIngestor  # noqa
from ingestors.postal_code_ingestor import PostalCodeIngestor  # noqa
from ingestors.ura_data_ingestor import URADataIngestor  # noqa
from ingestors.location_ingestor import LocationIngestor  # noqa
from ingestors.shophouse_ingestor import ShophouseIngestor  # noqa

log = logging.getLogger('root')
log.setLevel('DEBUG')
log.addHandler(CustomHandler())

BACKEND_HOST = os.environ.get("BACKEND_HOST", "backend:5000")

land_use_type_ingestor = LandUseTypeIngestor(BACKEND_HOST, "/landuse")
use_class_ingestor = UseClassIngestor(BACKEND_HOST, "/useclass")
past_case_ingestor = PastCaseIngestor(BACKEND_HOST, "/case")
location_ingestor = LocationIngestor(BACKEND_HOST, "/location")
ura_data_ingestor = URADataIngestor(past_case_ingestor, location_ingestor)
entity_pop_ingestor = EntityPopIngestor(BACKEND_HOST, "/entitypop")
guidelines_ingestor = GuidelinesIngestor(os.environ.get("GUIDELINES_CSV_FILE"))
postal_code_ingestor = PostalCodeIngestor(
    os.environ.get("POSTAL_CODE_JSON_FILE"),
    os.environ.get("HDB_COMMERCIAL_JSON_FILE"),
    os.environ.get("CONSERVED_BUILDING_JSON_FILE"),
    os.environ.get("SHOPHOUSE_JSON_FILE"),
    os.environ.get("LAND_USE_JSON_FILE")
)
shophouse_ingestor = ShophouseIngestor(os.environ.get("SHOPHOUSE_GUIDELINES_JSON_FILE"))


def init_guidelines():
    log.info("Initialising guidelines")
    guidelines_ingestor.ingest()


def init_postal_code():
    log.info("Initialising postal codes")
    postal_code_ingestor.ingest()


def init_shophouse():
    log.info("Initialising shophouse")
    shophouse_ingestor.ingest()


def init_use_class():
    log.info("Initialising generic use classes")
    use_class_ingestor.insert_generic()
    log.info("Initialising specific use classes")
    use_class_ingestor.insert_specific()
    log.info("Initialising examples for specific use classes")
    use_class_ingestor.ingest_specific_examples()


def init_land_use():
    log.info("Initialising generic land use type")
    land_use_type_ingestor.insert_generic()
    log.info("Initialising specific land use type")
    land_use_type_ingestor.insert_specific()


def init_past_cases(cases_directory):
    log.info("Initialising past cases")
    ura_data_ingestor.ingest_all(cases_directory)


def main():
    CASES_DATA_DIRECTORY = os.environ.get("CASES_DATA_DIRECTORY")

    if os.environ.get("INIT_SQL", "true").lower() == "true":
        log.info("initialising sql database")
        init_guidelines()
        init_postal_code()
        init_shophouse()

    if os.environ.get("INIT_GRAPH", "true").lower() == "true":
        log.info("initialising graph database")
        init_use_class()
        init_land_use()
        init_past_cases(CASES_DATA_DIRECTORY)


if __name__ == "__main__":
    log.info("starting ingestion")
    main()
