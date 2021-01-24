import os


DEBUG = True
SQLALCHEMY_DATABASE_URI = os.environ.get("SQL_DATABASE_URI", "mysql://user:password@0.0.0.0:5000/supa")
