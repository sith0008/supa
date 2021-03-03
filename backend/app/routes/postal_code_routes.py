from app import supa  # noqa
from app.services import postal_code_service  # noqa
from flask import request, jsonify
import logging

log = logging.getLogger('root')


@supa.route("/postal_code", methods=['GET'])
def get_postal_code():
    filter_map = dict(request.get_json())
    log.info(filter_map)
    postal_code = postal_code_service.get_postal_code(filter_map)
    return jsonify(postal_code)


@supa.route("/postal_code", methods=['PUT'])
def insert_postal_code():
    fields = dict(request.get_json())
    postal_code_service.insert_postal_code(fields)
    return f"postal_code {fields} inserted"


@supa.route("/postal_code", methods=['POST'])
def update_postal_code():
    fields = dict(request.get_json())
    postal_code_service.update_postal_code(fields)
    return f"postal_code {fields} updated"


@supa.route("/postal_code", methods=['DELETE'])
def delete_postal_code():
    fields = dict(request.get_json())
    postal_code_service.delete_postal_code(fields)
    return f"postal_code {fields} deleted"
