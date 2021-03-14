from ingestors.use_class import generic_use_classes, specific_use_class_map, use_class_details  # noqa
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
            if specific in use_class_details:
                info = use_class_details[specific]
                if "definition" in info:
                    data["definition"] = info["definition"]
                if "requirements" in info:
                    data["requirements"] = info["requirements"]

            res = requests.put(self.url, headers=headers, data=json.dumps(data))
            log.debug(f"request body: {res.request.body}")
            log.debug(f"status code: {res.status_code}")

    def ingest_specific_examples(self):
        headers = {
            'content-type': 'application/json'
        }
        for uc, info in use_class_details.items():
            data = {
                "specific_use_class": uc
            }
            if "examples" in info:
                for ex in info["examples"]:
                    data["name"] = ex
                    res = requests.put(self.url + "/example", headers=headers, data=json.dumps(data))
                    log.debug(f"request body: {res.request.body}")
                    log.debug(f"status code: {res.status_code}")


