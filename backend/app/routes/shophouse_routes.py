from app import supa  # noqa
from app.services import shophouse_service  # noqa
from flask import request, jsonify
import logging

log = logging.getLogger('root')


@supa.route("/shophouse", methods=['GET'])
def get_shophouse():
    filter_map = dict(request.args.items())
    shophouse = shophouse_service.get_shophouse(filter_map)
    return jsonify(shophouse)


@supa.route("/shophouse", methods=['PUT'])
def insert_shophouse():
    fields = dict(request.get_json())
    shophouse_service.insert_shophouse(fields)
    return f"Shophouse {fields} inserted"


@supa.route("/shophouse", methods=['POST'])
def update_shophouse():
    fields = dict(request.get_json())
    shophouse_service.update_shophouse(fields)
    return f"Shophouse {fields} updated"


@supa.route("/shophouse", methods=['DELETE'])
def delete_shophouse():
    fields = dict(request.get_json())
    shophouse_service.delete_shophouse(fields)
    return f"Shophouse {fields} deleted"
