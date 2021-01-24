from app import supa # noqa
from app.routes import * # noqa
from app.database import sql_db # noqa
import os

def init_sql_db(app):
    with app.app_context():
        sql_db.drop_all()
        sql_db.create_all()

if __name__ == "__main__":
    init_sql_db(supa)
    supa.config.from_pyfile('../config.py')
    supa.run(
        host=os.environ.get("BACKEND_HOST", "127.0.0.1"),
        port=os.environ.get("BACKEND_PORT", 5000)
    )