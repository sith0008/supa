import requests
import json


class GuidelinesAPI:
    def __init__(self, url):
        self.url = url

    def get_eval_outcome(self, property_type: str, use_class: str, is_agu: bool, is_pta: bool, is_pa: bool):

        headers = {
            'content-type': 'application/json'
        }
        data = {
            "business_use_type": use_class,
            "property_type": property_type
        }
        endpoint = "/guideline"
        res = requests.get(url=self.url + endpoint, headers=headers, data=json.dumps(data)).json()
        outcomes = []
        normal_outcome = None
        for outcome in res:
            if is_agu and outcome["conditions"] == 'AGU':
                outcomes.append(outcome)
            if is_pta and outcome["conditions"] == 'PTA':
                outcomes.append(outcome)
            if is_pa and outcome["conditions"] == 'Problematic Area':
                outcomes.append(outcome)
            if outcome["conditions"] == 'Normal':
                normal_outcome = outcome
        if not outcomes:
            outcomes.append(normal_outcome)
        return self.process_eval_outcomes(outcomes)

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

    def process_eval_outcomes(self, outcomes):
        worst_outcome = None
        worst_remark = None
        for outcome in outcomes:
            if not worst_outcome or self.compare_outcomes(outcome["outcome"], worst_outcome):
                worst_outcome = outcome["outcome"]
                worst_remark = outcome["remarks"]
        processed = f"Evaluation outcome: {worst_outcome} \n" \
                    f"Remarks: {worst_remark} \n"
        return processed

    def compare_outcomes(self, outcome_one, outcome_two):
        outcomes = {
            "Not Allowed": 1,
            "Unlikely": 2,
            "Submit Change Of Use Application": 3,
            "Instant Approval": 4,
            "No Planning Permission Required": 5,
        }
        return outcomes[outcome_one] < outcomes[outcome_two]

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