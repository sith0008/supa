# TODO: add class to make API calls for Knowledge Graph DB

class KnowledgeGraphAPI:
    def __init__(self, url):
        self.url = url

    def get_similar_cases(self, use_class: str, land_use_type: str):
        raise NotImplementedError

    def get_all_use_classes(self):
        raise NotImplementedError

    def validate_use_class(self, use_class: str):
        raise NotImplementedError

    def validate_postal_code(self, postal_code: int):
        raise NotImplementedError

    def get_locations(self, postal_code: int, floor: int, unit: int):
        raise NotImplementedError

    def get_property_type(self, postal_code: int, floor: int, unit: int, block: int, road: str):
        # query location DB, check booleans + land_use_type (rs)
        # create in-memory map here
        raise NotImplementedError