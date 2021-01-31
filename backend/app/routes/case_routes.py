from app import supa  # noqa
from app.services import cases_service  # noqa
from flask import request, jsonify
import logging

log = logging.getLogger('root')

@supa.route("/case", methods=['GET'])
def get_case():
    filter_map = dict(request.args.items())
    return jsonify(cases_service.get_case(filter_map))


@supa.route("/case", methods=['PUT'])
def insert_case():
    fields = dict(request.get_json())
    case_fields = fields["case"]
    location_fields = fields["location"]
    insert_case_id = cases_service.insert_case_with_location(case_fields, location_fields)
    print(insert_case_id)
    return f"inserted case with node id {insert_case_id}"


@supa.route("/case", methods=['POST'])
def update_case():
    fields = dict(request.get_json())
    update_case_id = cases_service.update_case(fields)
    print(update_case_id)
    return f"updated case with node id {update_case_id}"


@supa.route("/case", methods=['DELETE'])
def delete_case():
    case_id = dict(request.get_json())["case_id"]
    cases_service.delete_case(case_id)
    return f"deleted case with case id {case_id}"
