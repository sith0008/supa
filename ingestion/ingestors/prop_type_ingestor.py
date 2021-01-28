import requests
import json
from ingestors.property_type import generic_property_types, specific_property_type_map # noqa
import logging

log = logging.getLogger('root')

class PropertyTypeIngestor:
    def __init__(self, host, endpoint):
        self.url = host + endpoint

    def insert_generic(self):
        for generic_property_type in generic_property_types:
            headers = {
                'content-type':'application/json'
            }
            data = {
                "type": "Generic",
                "name": generic_property_type
            }
            res = requests.put(self.url, headers=headers, data=json.dumps(data))
            log.debug(f"status code: {res.status_code}")
            log.debug(f"request body: {res.request.body}")

    def insert_specific(self):
        for specific, generic in specific_property_type_map.items():
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