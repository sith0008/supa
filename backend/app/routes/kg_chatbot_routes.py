from app import supa  # noqa
from app.services import kg_chatbot_service  # noqa
from flask import request, jsonify
import logging

log = logging.getLogger('root')

@supa.route("/kg/chatbot/similar_cases", methods=['GET'])
def get_similar_cases():
    args = dict(request.args.items())

    return jsonify(kg_chatbot_service.get_similar_cases(
        args["specific_use_class"],
        args["block"],
        args["road"],
        args["postal_code"],
        args["floor"],
        args["unit"])
    )


