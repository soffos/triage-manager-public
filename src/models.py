from src import db

def dump_datetime(value):
  if value is None:
    return None
  return [value.strftime("%m-%d-%Y"), value.strftime("%H:%M:%S")]

class Reservation(db.Model):
  __tablename__ = "triagemgmt_reservations"
  id = db.Column(db.Integer, primary_key=True)
  uid = db.Column(db.String(32))
  name = db.Column(db.String(128))
  dow = db.Column(db.String(1))
  timeslot = db.Column(db.String(1))
  timestamp = db.Column(db.DateTime)
