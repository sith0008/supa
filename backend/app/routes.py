from app import supa
from app.services import cases_service
from flask import request, jsonify
import logging

log = logging.getLogger('root')

@supa.route("/", methods=['GET'])
def test():
    log.info("Received request")
    log.info("Processing request")
    log.info("Processed request")
    return "hello world."

# TODO: add more routes here when business logic is done
# EXAMPLE
# @supa.route("/cases", methods=['GET'])
# def get_cases():
#     cases = cases_service.get_cases()
#     return jsonify(cases)