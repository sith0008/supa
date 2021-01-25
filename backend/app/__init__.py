from flask import Flask
from app.database import sql_db # noqa
import os


supa = Flask(__name__)
supa.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQL_DATABASE_URI")
sql_db.init_app(supa)
