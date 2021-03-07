import requests
import json


class GuidelinesAPI:
    def __init__(self, url):
        self.url = url

    def get_eval_outcome(self, property_type: str, use_class: str):
        headers = {
            'content-type': 'application/json'
        }
        data = {
            "business_use_type": use_class,
            "property_type": property_type
        }
        endpoint = "/guidelines"
        res = requests.get(url=self.url + endpoint, headers=headers, data=json.dumps(data))
        return res.json()["outcome"]
