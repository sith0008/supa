from app import supa  # noqa
from app.services import problematic_area_service  # noqa
from flask import request, jsonify
import logging

log = logging.getLogger('root')


@supa.route("/problematic_area", methods=['GET'])
def get_problematic_area():
    filter_map = dict(request.args.items())
    problematic_area = problematic_area_service.get_problematic_area(filter_map)
    return jsonify(problematic_area)


@supa.route("/problematic_area", methods=['PUT'])
def insert_problematic_area():
    fields = dict(request.get_json())
    problematic_area_service.insert_problematic_area(fields)
    return f"Problematic Area {fields} inserted"


@supa.route("/problematic_area", methods=['POST'])
def update_problematic_area():
    fields = dict(request.get_json())
    problematic_area_service.update_problematic_area(fields)
    return f"Problematic Area {fields} updated"


@supa.route("/problematic_area", methods=['DELETE'])
def delete_problematic_area():
    fields = dict(request.get_json())
    problematic_area_service.delete_problematic_area(fields)
    return f"Problematic Area {fields} deleted"


@supa.route("/problematic_area/within", methods=['GET'])
def within_problematic_area():
    fields = dict(request.get_json())
    problematic_area = problematic_area_service.get_within(fields)
    return jsonify(problematic_area)
