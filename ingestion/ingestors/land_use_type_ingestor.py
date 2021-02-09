import requests
import json
from ingestors.land_use_type import generic_land_use_types, specific_land_use_type_map # noqa
import logging

log = logging.getLogger('root')

class LandUseTypeIngestor:
    def __init__(self, host, endpoint):
        self.url = host + endpoint

    def insert_generic(self):
        for generic_land_use_type in generic_land_use_types:
            headers = {
                'content-type':'application/json'
            }
            data = {
                "type": "Generic",
                "name": generic_land_use_type
            }
            res = requests.put(self.url, headers=headers, data=json.dumps(data))
            log.debug(f"status code: {res.status_code}")
            log.debug(f"request body: {res.request.body}")

    def insert_specific(self):
        for specific, generic in specific_land_use_type_map.items():
            headers = {
                'content-type': 'application/json'
            }
            data = {
                "type": "Specific",
                "name": specific,
                "generic": generic
            }
            res = requests.put(self.url, headers=headers, data=json.dumps(data))
            log.debug(f"status code: {res.status_code}")
            log.debug(f"request body: {res.request.body}")