import requests
import json

class LocationAPI:
    def __init__(self, url):
        self.url = url

    def is_valid_postal_code(self, postal_code):
        headers = {
        'content-type': 'application/json'
        }
        data = {
        "postal_code": postal_code,
        }
        endpoint = "/postal_code"
        res = requests.get(url=self.url + endpoint, headers=headers, data=json.dumps(data))
        return len(res.json()) > 0

    def get_addresses_from_postal_code(self, postal_code):
        headers = {
            'content-type': 'application/json'
        }
        data = {
            "postal_code": postal_code,
        }
        endpoint = "/postal_code"
        res = requests.get(url=self.url + endpoint, headers=headers, data=json.dumps(data))
        return res.json()

    def get_property_type_from_postal_code(self, postal_code: str):
        headers = {
            'content-type': 'application/json'
        }
        data = {
            "postal_code": postal_code,
        }
        endpoint = "/postal_code"
        res = requests.get(url=self.url + endpoint, headers=headers, data=json.dumps(data))
        return res.json()[0]["property_type"]