import requests
import json

class LocationAPI:
    def __init__(self, url):
        self.url = url

    def get_coordinates_from_postal_code(self, block, road, postal_code):
        headers = {
            'content-type': 'application/json'
        }
        data = {
            "block": block,
            "road": road,
            "postal_code": postal_code,
        }
        endpoint = "/postal_code"
        res = requests.get(url=self.url + endpoint, headers=headers, data=json.dumps(data))
        lat, lng = res.json()["latitude"], res.json()['longitude']
        return lat, lng

    def get_conditions(self, lat, lng):
        headers = {
            'content-type': 'application/json'
        }
        data = {
            "latitude": lat,
            "longitude": lng
        }
        is_agu = requests.get(url=self.url + "/activity_generating_use/within", headers=headers, data=json.dumps(data))
        is_pta = requests.get(url=self.url + "/problematic_traffic_area/within", headers=headers, data=json.dumps(data))
        is_pa = requests.get(url=self.url + "/problematic_area/within", headers=headers, data=json.dumps(data))
        return is_agu, is_pta, is_pa

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
