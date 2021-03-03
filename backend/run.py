from app import supa  # noqa
# add routes import here
from app.routes.test_routes import * # noqa
from app.routes.case_routes import * # noqa
from app.routes.guideline_routes import *  # noqa
from app.routes.postal_code_routes import *  # noqa
from app.routes.shophouse_routes import *  # noqa
from app.routes.use_class_routes import * # noqa
from app.routes.land_use_type_routes import * # noqa
from app.routes.location_routes import * # noqa
from app.routes.kg_chatbot_routes import * # noqa
from app.database import sql_db # noqa
import os
import logging
from app.commons.custom_logging import CustomHandler  # noqa

log = logging.getLogger('root')
log.setLevel('DEBUG')
log.addHandler(CustomHandler())


def init_sql_db(app):
    with app.app_context():
        sql_db.drop_all()
        sql_db.create_all()


if __name__ == "__main__":
    if os.environ.get("INGESTED").lower() == "false":
        init_sql_db(supa)
    supa.config.from_pyfile('../config.py')
    supa.run(
        host=os.environ.get("BACKEND_HOST", "127.0.0.1"),
        port=os.environ.get("BACKEND_PORT", 5000)
    )
