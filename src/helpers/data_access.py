from src import db, models

from datetime import datetime

# Returns: 
# Dict of dicts
#   each sub-dict has 3 timeslot keys
#     each timeslot key has list of names of triagers
#     default is ["?"]
# Ex:
#  reservations = {
#    "m": {
#      "1": ["?"],
#      "2": ["John Doe"],
#      "3": ["Jane Doe", "Joe Sixpack"]
#    },
#    "t": {
#      ...
#    },
#    ...
# }
def get_triage_reservations(initial_message=True, target_ts=None):
  if not initial_message:
    if target_ts is None:
      target_ts = get_target_ts()
    reservations = models.Reservation.query.filter(models.Reservation.target_slack_ts==str(target_ts)).all()

  ts=["1","2","3"]
  days=["mon","tue","wed","thu","fri"]
  resTemplate = {d:{t:[] for t in ts} for d in days}

  if not initial_message:
    for r in reservations:
      print("Adding {} to ts {} on day {}".format(r.name, r.timeslot, r.dow))
      resTemplate[r.dow][r.timeslot].append(r.name)

  for d,ts in resTemplate.items():
    for t,users in ts.items():
      if users==[]:
        resTemplate[d][t]=["?"]
  return resTemplate

def save_triage_reservation(data, message_ts):
  print(message_ts)
  reservations = []
  chosen_slot = data['actions'][0]['name'][-1:]
  for x in range(1, 4):
    if str(x) == chosen_slot or chosen_slot == "4":
      exists = models.Reservation.query.filter(models.Reservation.uid==data['user']['id'],
                                               models.Reservation.timeslot==str(x),
                                               models.Reservation.dow==data['actions'][0]['name'][:3],
                                               models.Reservation.target_slack_ts==str(message_ts)).first()
      print(exists)
      if not exists:
        print("Here with message_ts: {}".format(message_ts))
        reservations.append(
          models.Reservation(
            uid=data['user']['id'],
            name=data['user']['name'],
            dow=data['actions'][0]['name'][:3],
            timeslot=str(x),
            target_slack_ts=str(message_ts),
            timestamp=datetime.utcnow()
          )
        )
  for r in reservations:
    db.session.add(r)
  db.session.commit()

def get_target_ts():
  return models.Messages.query.order_by(models.Messages.slack_ts.desc())[0].slack_ts
