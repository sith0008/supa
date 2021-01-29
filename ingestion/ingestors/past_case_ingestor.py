import json
import logging
import requests
import os
from pathlib import Path

log = logging.getLogger('root')

class PastCaseIngestor:
    def __init__(self, host, endpoint):
        self.url = host + endpoint

    def ingest_all(self, case_directory):
        for path in Path(case_directory).rglob('*.json'):
            self.ingest_single_case(path.as_posix())

    def ingest_single_case(self, json_file_path):
        with open(json_file_path, "r") as f:
            data = json.load(f)
        if "bizTown" in data and "evalReport" in data:
            log.info(f"Inserting {json_file_path} into database")
            eval_data, proposal_data = data["evalReport"], data["bizTown"]
            req = self.construct_request(eval_data, proposal_data)
            headers = {
                'content-type': 'application/json'
            }
            res = requests.put(self.url, headers=headers, data=req)
            log.debug(f"status code: {res.status_code}")
            log.debug(f"request body: {res.request.body}")

        log.warning(f"{json_file_path} not added to database due to missing section")

    def construct_request(self, eval_data, proposal_data):
        req = {"case": {}, "location": {}}
        location_data = proposal_data["site_address_info"]["site_address"]
        mukim_data = proposal_data["mukim_ts_info"]["mukim_ts"]
        self.populate_case_data(req, location_data, mukim_data)
        self.populate_case_data(req, proposal_data, eval_data)
        return json.dumps(req)

    def populate_location_data(self, req, location_data, mukim_data):
        req["location"]["postal_code"] = location_data["postal_code"]
        req["location"]["floor"] = location_data["level"]
        req["location"]["unit"] = location_data["unit_no"]
        req["location"]["building_name"] = location_data["building_name"]
        req["location"]["lot_no"] = mukim_data["lot_no"]

    def populate_case_data(self, req, proposal_data, eval_data):
        req["case"]["case_id"] = proposal_data["submission_info"]["dc_ref"]
        req["case"]["proposed_use_desc"] = proposal_data["proposal_details_info"]["proposal_description"]
        cou_data =  proposal_data["change_of_use_info"]["cu_for_site_address"]["change_of_use"]
        req["case"]["use_class"] = cou_data["proposed_use_desc"].title()
        req["case"]["gfa"] = float(cou_data["use_gfa"])
        req["case"]["evaluation"] = eval_data["evaluation"]
        req["case"]["decision"] = eval_data["planningCont"]["decByAO"]



