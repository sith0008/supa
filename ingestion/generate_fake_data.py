from ingestors.land_use_type import specific_land_use_type_map # noqa
from ingestors.use_class import specific_use_class_map # noqa
import json

with open("Postal_Code.json") as f:
    postal_code_list = json.load(f)

def main():
    completed = 0
    quota_per_land_use = len(specific_use_class_map)
    land_use_type_counts = {}
    for specific_land_use in specific_land_use_type_map:
        land_use_type_counts[specific_land_use] = 0
    use_class_list = [uc for uc in specific_use_class_map]
    with open("Land_Use.json") as f:
        land_use_dict = json.load(f)
    i = 1
    for postal_code, land_uses in land_use_dict.items():
        if land_uses[0] in land_use_type_counts and land_use_type_counts[land_uses[0]] < quota_per_land_use:
            use_class = use_class_list[land_use_type_counts[land_uses[0]]]
            create_case(i, postal_code, use_class)
            i += 1
            land_use_type_counts[land_uses[0]] += 1
            if land_use_type_counts[land_uses[0]] == quota_per_land_use:
                completed += 1

            if completed == len(land_use_type_counts):
                break

def create_case(case_id, postal_code, use_class):
    print(f"creating case {case_id} with postal code {postal_code} and use class {use_class}")
    addr_details = postal_code_list[postal_code][0]

    case_data = {
        "evalReport": [{
            "evaluation": f"EVALUATION DESCRIPTION FOR CASE {case_id}",
            "planningEvalParam": "FURTHER EVALUATION DETAILS ...",
            "planningCont": [{
                "poRemarks": "Recommended to issue Advice/TP/WP",
                "decByAO": "Approved"
            }]
        }],
        "bizTown": [{
            "application_code": "DACU",
            "application_desc": "Change of Use",
            "submission_info": {
                "dc_ref": f"{case_id}",
                "planning_area_code": "KL",
                "planning_area_desc": "KALLANG",
            },
            "mukim_ts_info": {
                "mukim_ts": {
                    "lot_no": f"{case_id}",
                    "mk_ts_flag": "TS",
                    "mk_ts_no": 1,
                    "park_lot_ind": "N"
                }
            },
            "site_address_info": {
                "site_address": {
                    "site_address_id": 1,
                    "road_name": addr_details["ROAD_NAME"],
                    "house_no": addr_details["BLK_NO"],
                    "unit_no": 1,
                    "level": 1,
                    "postal_code": postal_code,
                    "core_area_ind": "N"
                }
            },
            "proposal_details_info": {
                "proposal_description": "Change of Use of A to B",
            },
            "change_of_use_info": {
                "cu_for_site_address": {
                    "site_address": 1,
                    "change_of_use": {
                        "seq_no": 1,
                        "proposed_use_code": use_class,
                        "proposed_use_desc": use_class,
                        "use_gfa": 54.86,
                    }
                }
            }

        }]
    }
    with open(f"./sample/{case_id}.json", "w") as f:
        json.dump(case_data, f)

if __name__ == '__main__':
    main()