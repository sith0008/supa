from ingestors.past_case_ingestor import PastCaseIngestor # noqa
from ingestors.location_ingestor import LocationIngestor # noqa
import json
import logging
import requests
from pathlib import Path

log = logging.getLogger('root')

class URADataIngestor:
    def __init__(self, past_case_ingestor: PastCaseIngestor, location_ingestor: LocationIngestor):
        self.past_case_ingestor = past_case_ingestor
        self.location_ingestor = location_ingestor

    def ingest_all(self, case_directory):
        for path in Path(case_directory).rglob('*.json'):
            self.ingest_single_case(path.as_posix())

    def ingest_single_case(self, json_file_path):
        with open(json_file_path, "r") as f:
            data = json.load(f)
        if "bizTown" in data and "evalReport" in data:
            log.info(f"Inserting {json_file_path} into database")
            eval_data, proposal_data = data["evalReport"], data["bizTown"]
            self.location_ingestor.ingest(proposal_data)
            self.past_case_ingestor.ingest(eval_data, proposal_data)

        log.warning(f"{json_file_path} not added to database due to missing section")




