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
