from src import db

def dump_datetime(value):
  if value is None:
    return None
  return [value.strftime("%m-%d-%Y"), value.strftime("%H:%M:%S")]

# This table is designed to keep track of triage block reservations
# Each row will refer to a singular individual's reservation in a singular timeslot (hour within a day of the week)
class Reservation(db.Model):
  __tablename__ = "triagemgmt_reservations"
  id = db.Column(db.Integer, primary_key=True)
  uid = db.Column(db.String(32))
  name = db.Column(db.String(128))
  dow = db.Column(db.String(3))
  timeslot = db.Column(db.String(1))
  target_slack_ts = db.Column(db.String(128))
  timestamp = db.Column(db.DateTime)

  @property
  def serialize(self):
    return {
      'id': self.id,
      'uid': self.uid,
      'name': self.name,
      'dow': self.dow,
      'timeslot': self.timeslot,
      'slack_ts': self.target_slack_ts,
      'timestamp': dump_datetime(self.timestamp)
    }

# Track delivered slack messages and timestamps
# Designed to facilitate update of triage messages
class Messages(db.Model):
  __tablename__ = "triagemgmt_messages"
  id = db.Column(db.Integer, primary_key=True)
  slack_ts = db.Column(db.String(128))

class Metadata(db.Model):
  __tablename__ = 'triagemgmt_metadata'
  id = db.Column(db.Integer, primary_key=True)
  channel_id = db.Column(db.String(32))
  app_id = db.Column(db.String(32))
  bot_id = db.Column(db.String(32))
  calendar_id = db.Column(db.String(128))
  api_base = db.Column(db.String(128))
