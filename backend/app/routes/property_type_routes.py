from app import supa # noqa
from app.services import property_type_service # noqa
from flask import request, jsonify
import logging

log = logging.getLogger('root')

@supa.route("/proptype", methods=['GET'])
def get_property_type():
    filter_map = dict(request.args.items())
    return jsonify(property_type_service.get(filter_map))

@supa.route("/proptype", methods=['PUT'])
def insert_property_type():
    fields = dict(request.get_json())
    insert_property_type_id = property_type_service.create(fields)
    return f"inserted property type with node id {insert_property_type_id}"

@supa.route("/proptype", methods=['DELETE'])
def delete_property_type():
    fields = dict(request.get_json())
    property_type_service.delete(fields['name'], fields['type'])
    return f"deleted {fields['type']} property type {fields['name']}"
