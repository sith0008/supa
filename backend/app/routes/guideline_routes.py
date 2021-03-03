from app import supa  # noqa
from app.services import guidelines_service  # noqa
from flask import request, jsonify
import logging

log = logging.getLogger('root')


@supa.route("/guideline", methods=['GET'])
def get_guidelines():
    filter_map = dict(request.get_json())
    guideline = guidelines_service.get_guidelines(filter_map)
    return jsonify(guideline)


@supa.route("/guideline", methods=['PUT'])
def insert_guideline():
    fields = dict(request.get_json())
    guidelines_service.insert_guideline(fields)
    return f"Guideline {fields} inserted"


@supa.route("/guideline", methods=['POST'])
def update_guideline():
    fields = dict(request.get_json())
    guidelines_service.update_guideline(fields)
    return f"Guideline {fields} updated"


@supa.route("/guideline", methods=['DELETE'])
def delete_guideline():
    fields = dict(request.get_json())
    guidelines_service.delete_guideline(fields)
    return f"Guideline {fields} deleted"
