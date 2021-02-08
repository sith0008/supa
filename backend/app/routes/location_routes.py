from app import supa  # noqa
from app.services import location_service  # noqa
from flask import request, jsonify
import logging

log = logging.getLogger('root')


@supa.route("/location/address", methods=['GET'])
def get_location():
    filter_map = dict(request.args.items())
    return location_service.get_address(filter_map)


@supa.route("/location", methods=['GET'])
def get_location():
    filter_map = dict(request.args.items())
    return jsonify(location_service.get_location(filter_map))


@supa.route("/location", methods=['PUT'])
def insert_location():
    fields = dict(request.get_json())
    insert_location_id = location_service.insert_location(fields)
    return f"inserted location with node id {insert_location_id}"


@supa.route("/location", methods=['POST'])
def update_location():
    fields = dict(request.get_json())
    update_location_id = location_service.update_location(fields)
    return f"updated location with node id {update_location_id}"


@supa.route("/location", methods=['DELETE'])
def delete_location():
    fields = dict(request.get_json())
    location_service.delete_location(fields)
    return f"deleted location with location {fields}"
