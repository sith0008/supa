from app import supa # noqa
from app.services import land_use_type_service # noqa
from flask import request, jsonify
import logging

log = logging.getLogger('root')

@supa.route("/landuse", methods=['GET'])
def get_land_use_type():
    filter_map = dict(request.args.items())
    return jsonify(land_use_type_service.get(filter_map))

@supa.route("/landuse", methods=['PUT'])
def insert_land_use_type():
    fields = dict(request.get_json())
    insert_land_use_type_id = land_use_type_service.create(fields)
    return f"inserted land use type with node id {insert_land_use_type_id}"

@supa.route("/landuse", methods=['DELETE'])
def delete_land_use_type():
    fields = dict(request.get_json())
    land_use_type_service.delete(fields['name'], fields['type'])
    return f"deleted {fields['type']} land use type {fields['name']}"
