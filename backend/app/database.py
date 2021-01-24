from flask_sqlalchemy import SQLAlchemy
from py2neo.ogm import Repository
import os


sql_db = SQLAlchemy()
graph_db = Repository(
    os.environ.get("GRAPH_DATABASE_URI", "bolt://localhost:7687"),
    password=os.environ.get("GRAPH_DATABASE_PASSWORD", "password")
)