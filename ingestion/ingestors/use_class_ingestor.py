from ingestors.use_class import generic_use_classes, specific_use_class_map  # noqa
import requests
import json


class UseClassIngestor:
    def __init__(self, host, endpoint):
        self.url = host + endpoint

    def insert_generic(self):
        for generic_use_class in generic_use_classes:
            data = {
                "type": "Generic",
                "name": generic_use_class
            }
            _ = requests.post(self.url, data=json.dumps(data))

    def insert_specific(self):
        for specific, generic in specific_use_class_map.items():
            data = {
                "type": "Specific",
                "name": specific,
                "generic": generic
            }
            _ = requests.post(self.url, data=json.dumps(data))