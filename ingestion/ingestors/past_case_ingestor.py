import json
import logging
import requests
from pathlib import Path

log = logging.getLogger('root')

class PastCaseIngestor:
    def __init__(self, host, endpoint):
        self.url = host + endpoint

    def ingest(self, eval_data, proposal_data):
        req = self.construct_case_request(eval_data, proposal_data)
        headers = {
            'content-type': 'application/json'
        }
        res = requests.put(self.url, headers=headers, data=req)
        log.debug(f"status code: {res.status_code}")
        log.debug(f"request body: {res.request.body}")

    def construct_case_request(self, eval_data, proposal_data):
        req = {"case": {}, "location": {}, "use_class": {}}
        location_data = proposal_data["site_address_info"]["site_address"]
        self.populate_location_key_data(req, location_data)
        self.populate_case_data(req, proposal_data, eval_data)
        return json.dumps(req)

    def populate_location_key_data(self, req, location_data):
        req["location"]["block"] = location_data["house_no"]
        req["location"]["road"] = location_data["road_name"]
        req["location"]["postal_code"] = location_data["postal_code"]
        req["location"]["floor"] = location_data["level"]
        req["location"]["unit"] = location_data["unit_no"]

    def populate_case_data(self, req, proposal_data, eval_data):
        req["case"]["case_id"] = proposal_data["submission_info"]["dc_ref"]
        req["case"]["proposed_use_desc"] = proposal_data["proposal_details_info"]["proposal_description"]
        req["case"]["evaluation"] = eval_data["evaluation"]
        req["case"]["decision"] = eval_data["planningCont"][0]["decByAO"]
        cou_data =  proposal_data["change_of_use_info"]["cu_for_site_address"]["change_of_use"]
        req["case"]["gfa"] = float(cou_data["use_gfa"])
        req["use_class"]["name"] = cou_data["proposed_use_desc"]