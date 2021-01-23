from app import supa
from flask import request, jsonify

@supa.route("/", methods=['GET'])
def test():
    return "hello world."

# TODO: add more routes here when business logic is done
# EXAMPLE
# @supa.route("/cases", methods=['GET'])
# def get_cases():
#     cases = cases_service.get_cases()
#     return jsonify(cases)