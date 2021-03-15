from app import supa  # noqa
from app.services import activity_generating_use_service  # noqa
from flask import request, jsonify
import logging

log = logging.getLogger('root')


@supa.route("/activity_generating_use", methods=['GET'])
def get_activity_generating_use():
    filter_map = dict(request.args.items())
    activity_generating_use = activity_generating_use_service.get_activity_generating_use(filter_map)
    return jsonify(activity_generating_use)


@supa.route("/activity_generating_use", methods=['PUT'])
def insert_activity_generating_use():
    fields = dict(request.get_json())
    activity_generating_use_service.insert_activity_generating_use(fields)
    return f"Activity Generating Use {fields} inserted"


@supa.route("/activity_generating_use", methods=['POST'])
def update_activity_generating_use():
    fields = dict(request.get_json())
    activity_generating_use_service.update_activity_generating_use(fields)
    return f"Activity Generating Use {fields} updated"


@supa.route("/activity_generating_use", methods=['DELETE'])
def delete_activity_generating_use():
    fields = dict(request.get_json())
    activity_generating_use_service.delete_activity_generating_use(fields)
    return f"Activity Generating Use {fields} deleted"


@supa.route("/activity_generating_use/within", methods=['GET'])
def within_activity_generating_use():
    fields = dict(request.get_json())
    activity_generating_use = activity_generating_use_service.get_within(fields)
    return jsonify(activity_generating_use)
