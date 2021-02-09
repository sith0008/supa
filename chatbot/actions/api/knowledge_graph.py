# TODO: add class to make API calls for Knowledge Graph DB
import requests
import json

class KnowledgeGraphAPI:
    def __init__(self, url):
        self.url = url

    @staticmethod
    def get_similar_cases(self, use_class: str, land_use_type: str):
        # TODO: implement after kg chatbot service branch is merged
        headers = {
            'content-type': 'application/json'
        }
        data = {
            "land_use_type": "",
            "use_class": ""
        }
        return ""

    @staticmethod
    def get_all_use_classes(self):
        headers = {
            'content-type': 'application/json'
        }
        data = {
            "type": "multiple",
            "query": "Specific"
        }
        res = requests.get(url=self.url, headers=headers, data=json.dumps(data))
        # TODO: add processing, format to a readable list
        return res

    @staticmethod
    def is_valid_use_class(self, use_class: str):
        headers = {
            'content-type': 'application/json'
        }
        data = {
            "type": "single",
            "query": use_class
        }
        res = requests.get(url=self.url, headers=headers, data=json.dumps(data))
        return res is not None

    @staticmethod
    def get_locations(self, postal_code: int, floor: int, unit: int):
        raise NotImplementedError

    @staticmethod
    def get_property_type(self, postal_code: int, floor: int, unit: int, block: int, road: str):
        # query location DB, check booleans + land_use_type (rs)
        # create in-memory map here
        raise NotImplementedError