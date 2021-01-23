# TODO: add data model for guidelines here
# use SQLAlchemy

from backend.app.database import db
from sqlalchemy import (
    Column,
    Text
)

class Guideline(db.Model):
    # TODO: add other fields here
    use_class = Column(Text)