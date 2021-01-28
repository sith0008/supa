import os
import logging
from commons.custom_logging import CustomHandler  # noqa

from ingestors.prop_type_ingestor import PropertyTypeIngestor # noqa
from ingestors.use_class_ingestor import UseClassIngestor # noqa
from ingestors.past_case_ingestor import PastCaseIngestor # noqa
from ingestors.entity_pop_ingestor import EntityPopIngestor # noqa
from ingestors.guidelines_ingestor import GuidelinesIngestor # noqa

log = logging.getLogger('root')
log.setLevel('DEBUG')
log.addHandler(CustomHandler())

BACKEND_HOST = os.environ.get("BACKEND_HOST", "backend:5000")

prop_type_ingestor = PropertyTypeIngestor(BACKEND_HOST, "/proptype")
use_class_ingestor = UseClassIngestor(BACKEND_HOST, "/useclass")
past_case_ingestor = PastCaseIngestor(BACKEND_HOST, "/case")
entity_pop_ingestor = EntityPopIngestor(BACKEND_HOST, "/entitypop")
guidelines_ingestor = GuidelinesIngestor(BACKEND_HOST, "/guideline")


def main():
    GUIDELINES_CSV_FILE = os.environ.get("GUIDELINES_CSV_FILE")
    CASES_DATA_DIRECTORY = os.environ.get("INPUT_DATA_DIR")
    if os.environ.get("INIT_SQL", "true").lower() == "true":
        # TODO: call methods from guidelines_ingestor
        log.info("initialising guidelines database")
        guidelines_ingestor.ingest(GUIDELINES_CSV_FILE)

    # if os.environ.get("INIT_GRAPH", "true").lower() == "true":
    #     # TODO: call methdos from prop_type_ingestor, use_class_ingestor, past_case_ingestor, entity_pop_ingestor
    #     log.info("initialising graph database")
    #     raise NotImplementedError


if __name__ == "__main__":
    log.info("starting ingestion")
    main()
