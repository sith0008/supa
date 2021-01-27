from app import supa # noqa
from app.services import use_class_service # noqa
from flask import request, jsonify
import logging

log = logging.getLogger('root')

@supa.route("/useclass", methods=['GET'])
def get_use_class():
    filter_map = dict(request.args.items())
    return jsonify(use_class_service.get(filter_map))

@supa.route("/useclass", methods=['PUT'])
def insert_use_class():
    fields = dict(request.get_json())
    insert_use_class_id = use_class_service.create(fields)
    return f"inserted use class with node id {insert_use_class_id}"

@supa.route("/useclass", methods=['DELETE'])
def delete_use_class():
    fields = dict(request.get_json())
    use_class_service.delete(fields['name'], fields['type'])
    return f"deleted {fields['type']} use class {fields['name']}"
