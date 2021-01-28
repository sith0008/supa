import os
import logging
from commons.custom_logging import CustomHandler  # noqa

log = logging.getLogger('root')
log.setLevel('DEBUG')
log.addHandler(CustomHandler())


def main():
    GUIDELINES_CSV_FILE = os.environ.get("INPUT_CSV")
    CASES_DATA_DIRECTORY = os.environ.get("INPUT_DATA_DIR")

    if os.environ.get("INIT_SQL", "true").lower() == "true":
        # TODO: run init guideline method
        log.info("initialising guidelines database")
        raise NotImplementedError

    if os.environ.get("INIT_GRAPH", "true").lower() == "true":
        # TODO: run init graph nodes methods
        log.info("initialising graph database")
        raise NotImplementedError


if __name__ == "__main__":
    log.info("starting ingestion")
    main()