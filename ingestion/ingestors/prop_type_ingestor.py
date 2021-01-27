import requests
import json
from ingestors.property_type import generic_property_types, specific_property_type_map # noqa


class PropertyTypeIngestor:
    def __init__(self, host, endpoint):
        self.url = host + endpoint

    def insert_generic(self):
        for generic_property_type in generic_property_types:
            data = {
                "type": "Generic",
                "name": generic_property_type
            }
            _ = requests.post(self.url, data=json.dumps(data))

    def insert_specific(self):
        for specific, generic in specific_property_type_map.items():
            data = {
                "type": "Specific",
                "name": specific,
                "generic": generic
            }
            _ = requests.post(self.url, data=json.dumps(data))
