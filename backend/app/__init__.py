from flask import Flask
from app.database import db

supa = Flask(__name__)
db.init_app(supa)