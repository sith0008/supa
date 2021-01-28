from ingestors.use_class import generic_use_classes, specific_use_class_map  # noqa
import requests
import json
import logging

log = logging.getLogger('root')


class UseClassIngestor:
    def __init__(self, host, endpoint):
        self.url = host + endpoint

    def insert_generic(self):
        for generic_use_class in generic_use_classes:
            headers = {
                'content-type': 'application/json'
            }
            data = {
                'type': 'Generic',
                'name': generic_use_class
            }
            res = requests.put(self.url, headers=headers, data=json.dumps(data))
            log.debug(f"request body: {res.request.body}")
            log.debug(f"status code: {res.status_code}")

    def insert_specific(self):
        for specific, generic in specific_use_class_map.items():
            headers = {
                'content-type': 'application/json'
            }
            data = {
                'type': 'Specific',
                'name': specific,
                'generic': generic
            }
            res = requests.put(self.url, headers=headers, data=json.dumps(data))
            log.debug(f"request body: {res.request.body}")
            log.debug(f"status code: {res.status_code}")