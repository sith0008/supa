from app import supa  # noqa
from app.services import property_type_service  # noqa
from flask import request, jsonify
import logging

log = logging.getLogger('root')


@supa.route("/property_type", methods=['GET'])
def get_property_type():
    filter_map = dict(request.args.items())
    property_type = property_type_service.get_property_type(filter_map)
    return jsonify(property_type)


@supa.route("/property_type", methods=['PUT'])
def insert_property_type():
    fields = dict(request.get_json())
    property_type_service.insert_property_type(fields)
    return f"Property_type {fields} inserted"


@supa.route("/property_type", methods=['POST'])
def update_property_type():
    fields = dict(request.get_json())
    property_type_service.update_property_type(fields)
    return f"Property_type {fields} updated"


@supa.route("/property_type", methods=['DELETE'])
def delete_property_type():
    fields = dict(request.get_json())
    property_type_service.delete_property_type(fields)
    return f"Property_type {fields} deleted"
