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
        endpoint = "/guideline"
        res = requests.get(url=self.url + endpoint, headers=headers, data=json.dumps(data))
        # TODO:
        return res.json()[0]["outcome"]

    # TODO: query shophouse service
    def get_shophouse_eval_outcome(self, block, road, postal_code, use_class):
        raise NotImplementedError