import requests
import json

class LocationAPI:
    def __init__(self, url):
        self.url = url

    def is_valid_postal_code(self, postal_code):
        # TODO: to implement after location DB is setup
        raise NotImplementedError

    def get_addresses_from_postal_code(self, postal_code):
        # TODO: to implement after location DB is setup
        raise NotImplementedError

    def get_land_use_type_from_addr(self,
                                    block: str,
                                    road: str,
                                    postal_code: int,
                                    floor: int,
                                    unit: int
                                    ):
        headers = {
            'content-type': 'application/json'
        }
        data = {
            "query_by": "location",
            "block": block,
            "road": road,
            "postal_code": postal_code,
            "floor": floor,
            "unit": unit
        }
        endpoint = "/landuse"
        res = requests.get(url=self.url + endpoint, headers=headers, data=json.dumps(data))
        return res