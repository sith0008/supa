from ingestors.use_class import generic_use_classes, specific_use_class_map  # noqa
import requests
import json
import logging

log = logging.getLogger('root')


class UseClassIngestor:
    def __init__(self, host, endpoint):
        self.url = host + endpoint

    def ingest(self, proposal_data):
        req = self.construct_location_request(proposal_data)
        headers = {
            'content-type': 'application/json'
        }
        res = requests.put(self.url, headers=headers, data=req)
        log.debug(f"status code: {res.status_code}")
        log.debug(f"request body: {res.request.body}")

    def construct_location_request(self, proposal_data):
        req = {"location": {}, "property_type": {}}
        location_data = proposal_data["site_address_info"]["site_address"]
        mukim_data = proposal_data["mukim_ts_info"]["mukim_ts"]
        self.populate_location_data(req, location_data, mukim_data)
        return json.dumps(req)

    def populate_location_key_data(self, req, location_data):
        req["location"]["postal_code"] = location_data["postal_code"]
        req["location"]["floor"] = location_data["level"]
        req["location"]["unit"] = location_data["unit_no"]

    def populate_location_data(self, req, location_data, mukim_data):
        self.populate_location_key_data(req, location_data)
        req["location"]["building_name"] = location_data["building_name"]
        req["location"]["lot_no"] = mukim_data["lot_no"]
