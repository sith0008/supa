from app import supa # noqa
import logging

log = logging.getLogger('root')

@supa.route("/", methods=['GET'])
def test():
    log.info("Received request")
    log.info("Processing request")
    log.info("Processed request")
    return "hello world."