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
        return [{"Case 1": "ABC"}, {"Case 2": "XYZ"}]
        # TODO: implement after kg chatbot service branch is merged
        headers = {
            'content-type': 'application/json'
        }
        data = {
            "specific_use_class": use_class,
            "postal_code": postal_code,
        }
        endpoint = "/kg/chatbot/similar_cases"
        res = requests.get(url=self.url+endpoint, headers=headers, data=json.dumps(data))
        return res

    def get_all_use_classes(self):
        return [{"Use class 1": "ABC"}, {"Use class 2": "XYZ"}]
        headers = {
            'content-type': 'application/json'
        }
        data = {
            "type": "multiple",
            "query": "Specific"
        }
        endpoint = "/useclass"
        res = requests.get(url=self.url+endpoint, headers=headers, data=json.dumps(data))
        # TODO: add processing, format to a readable list
        return res

    def is_valid_use_class(self, use_class: str):
        use_class_list = [
            "Restaurant",
            "Pet Shop",
            "Office"
        ]
        return use_class in use_class_list
        headers = {
            'content-type': 'application/json'
        }
        data = {
            "type": "single",
            "query": use_class
        }
        endpoint = "/useclass"
        res = requests.get(url=self.url+endpoint, headers=headers, data=json.dumps(data))
        return res is not None

    def get_locations(self, postal_code: int, floor: str, unit: str):
        raise NotImplementedError

    def get_property_type(self, postal_code: int, floor: str, unit: str, block: str, road: str):
        # query location DB, check booleans + land_use_type (rs)
        # create in-memory map here
        raise NotImplementedError