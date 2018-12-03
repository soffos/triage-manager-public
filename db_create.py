#!venv/bin/python
from src import db, models

db.create_all()
db.session.commit()
