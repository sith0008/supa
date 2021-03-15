# TODO: add class to make API calls for Knowledge Graph DB
import requests
import json

class KnowledgeGraphAPI:
    def __init__(self, url):
        self.url = url

    def process_case_results(self, similar_case_results):
        processed_list = "\n"
        for i, res in enumerate(similar_case_results):
            processed = f"{i+1}. Case {res['case']['case_id']}: {res['case']['proposed_use_desc']} \n\n"
            processed += f"Address: {res['location']['block']} {res['location']['road']}, {res['location']['postal_code']} \n"
            processed += f"Land use type: {res['land_use_type']['specific']} \n"
            processed += f"Proposed use class: {res['use_class']['specific']} \n"
            processed += f"Gross floor area: {res['case']['gfa']} \n"
            processed += f"Decision: {res['case']['decision']} \n"
            processed += f"Evaluation: {res['case']['evaluation']} \n\n\n"
            processed_list += processed

        return processed_list

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
        res = requests.get(url=self.url+endpoint, headers=headers, params=data)
        return self.process_case_results(res.json())

    def get_all_use_classes(self):
        headers = {
            'content-type': 'application/json'
        }
        data = {
            "type": "multiple",
            "query": "Specific"
        }
        endpoint = "/useclass"
        res = requests.get(url=self.url+endpoint, headers=headers, params=data)
        use_classes_str = ""
        for i, uc in enumerate(res.json()):
            use_classes_str += f"{i+1}. {uc} \n"
        return use_classes_str

    def is_valid_use_class(self, use_class: str):
        headers = {
            'content-type': 'application/json'
        }
        data = {
            "type": "multiple",
            "query": "Specific"
        }
        endpoint = "/useclass"
        res = requests.get(url=self.url+endpoint, headers=headers, params=data)
        return use_class.lower() in [uc.lower() for uc in res.json()]

    def get_locations(self, postal_code: int, floor: str, unit: str):
        raise NotImplementedError

    def get_property_type(self, postal_code: int, floor: str, unit: str, block: str, road: str):
        # query location DB, check booleans + land_use_type (rs)
        # create in-memory map here
        raise NotImplementedError

    def get_definition(self, use_class):
        headers = {
            'content-type': 'application/json'
        }
        data = {
            "type": "single",
            "query": use_class,
        }
        endpoint = "/useclass"
        res = requests.get(url=self.url+endpoint, headers=headers, params=data)
        return res.json()["definition"]

    def get_requirements(self, use_class):
        headers = {
            'content-type': 'application/json'
        }
        data = {
            "type": "single",
            "query": use_class,
        }
        endpoint = "/useclass"
        res = requests.get(url=self.url+endpoint, headers=headers, params=data)
        return res.json()["requirements"]

    def get_examples(self, use_class):
        headers = {
            'content-type': 'application/json'
        }
        data = {
            "specific_use_class": use_class
        }
        endpoint = "/useclass/example"
        res = requests.get(url=self.url+endpoint, headers=headers, params=data)
        examples_str = ""
        for i, ex in enumerate(res.json()):
            examples_str += f"{i+1}. {ex} \n"
        return examples_str