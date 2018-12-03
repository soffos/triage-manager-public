from src import db, models

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
def get_triage_reservations(initial_message=True):
  if not initial_message:
    target_ts = get_target_ts()
    reservations = models.Reservation.query.filter(models.Reservation.target_slack_ts==target_ts).all()

  ts=["1","2","3"]
  days=["m","t","w","h","f"]
  resTemplate = {d:{t:[] for t in ts} for d in days}

  import pprint;pp=pprint.PrettyPrinter()
  pp.pprint(resTemplate)
  if not initial_message:
    for r in reservations:
      print("Adding {} to ts {} on day {}".format(r.name, r.timeslot, r.dow))
      resTemplate[r.dow][r.timeslot].append(r.name)

  for d,ts in resTemplate.items():
    for t,users in ts.items():
      if users==[]:
        resTemplate[d][t]=["?"]
  pp.pprint(resTemplate)
  return resTemplate

def save_triage_reservation(data):
  reservations = []
  chosen_slot = data['actions'][0]['value']
  import pprint;pp=pprint.PrettyPrinter()
  pp.pprint(data)
  for x in range(1, 4):
    if str(x) == chosen_slot or chosen_slot == "4":
      exists = models.Reservation.query.filter(models.Reservation.uid==data['user']['id'],
                                               models.Reservation.timeslot==str(x),
                                               models.Reservation.dow==data['actions'][0]['name'][0]).first()
      if not exists:
        reservations.append(
          models.Reservation(
            uid=data['user']['id'],
            name=data['user']['name'],
            dow=data['actions'][0]['name'][0],
            timeslot=str(x),
            target_slack_ts=get_target_ts()
          )
        )
  for r in reservations:
    db.session.add(r)
  db.session.commit()

def get_target_ts():
  return models.Messages.query.order_by(models.Messages.slack_ts.desc())[0].slack_ts
