from app.database import sql_db
from sqlalchemy import (
    Column,
    Text,
    Integer
)


class Guideline(sql_db.Model):
    # TODO: change fields accordingly, placeholder for testing
    id = Column(Integer,  primary_key=True)
    use_class = Column(Text)
