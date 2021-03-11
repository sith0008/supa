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
        return self.process_eval_outcome(res.json()[0])

    # TODO: query shophouse service
    def get_shophouse_eval_outcome(self, block, road, floor, unit, use_class):
        headers = {
            'content-type': 'application/json'
        }
        data = {
            "block": block,
            "road": road,
            "floor": floor,
            "unit": unit,
            "use_class": use_class
        }
        endpoint = "/shophouse"
        res = requests.get(url=self.url + endpoint, headers=headers, params=data)

        return self.process_shophouse_eval_outcome(res.json())

    def process_eval_outcome(self, result):
        outcome = result["outcome"]
        remark = result["remarks"]
        processed = f"Evaluation outcome: {outcome} \n" \
                    f"Remarks: {remark} \n"
        return processed

    def process_shophouse_eval_outcome(self, result):
        outcome_map = {
            "Y": "Allowed",
            "N": "Not allowed",
            "M": "Submit for evaluation"
        }
        outcome = outcome_map[result["allowed"]]
        remark = result["reason"]
        processed = f"Evaluation outcome: {outcome} \n" \
                    f"Remarks: {remark} \n"
        return processed