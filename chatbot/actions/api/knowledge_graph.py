# TODO: add class to make API calls for Knowledge Graph DB
import requests
import json

class KnowledgeGraphAPI:
    def __init__(self, url):
        self.url = url

    def get_similar_cases(self,
                          use_class: str,
                          postal_code: int,
                          ):
        headers = {
            'content-type': 'application/json'
        }
        data = {
            "specific_use_class": use_class,
            "postal_code": postal_code,
        }
        endpoint = "/kg/chatbot/similar_cases"
        res = requests.get(url=self.url+endpoint, headers=headers, data=json.dumps(data))
        return res.json()

    def get_all_use_classes(self):
        headers = {
            'content-type': 'application/json'
        }
        data = {
            "type": "multiple",
            "query": "Specific"
        }
        endpoint = "/useclass"
        res = requests.get(url=self.url+endpoint, headers=headers, data=json.dumps(data))
        return [uc["name"] for uc in res.json()]

    def is_valid_use_class(self, use_class: str):
        headers = {
            'content-type': 'application/json'
        }
        data = {
            "type": "multiple",
            "query": "Specific"
        }
        endpoint = "/useclass"
        res = requests.get(url=self.url+endpoint, headers=headers, data=json.dumps(data))
        print(res.json())
        use_class_list = [uc["name"].lower() for uc in res.json()]
        return use_class.lower() in use_class_list

    def get_locations(self, postal_code: int, floor: str, unit: str):
        raise NotImplementedError

    def get_property_type(self, postal_code: int, floor: str, unit: str, block: str, road: str):
        # query location DB, check booleans + land_use_type (rs)
        # create in-memory map here
        raise NotImplementedError