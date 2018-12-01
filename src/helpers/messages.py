import src.helpers.constants as CONST
from src.helpers import data_access

def post_weekly_message(slack):
  # Dict of dicts
  #   each sub-dict has 3 timeslot keys
  #     each timeslot key has list of names of triagers
  #     default is empty list
  # Ex:
  #  reservations = {
  #    "m": {
  #      "1": [],
  #      "2": [],
  #      "3": []
  #    },
  #    "t": {
  #      ...
  #    },
  #    ...
  # }
  reservations = data_access.get_triager_reservations()
  msg_values = []
  for dow in ["m","t","w","h","f"]:
    for t in range(1,4):
      msg_values.extend(reservations[dow][str(t)])

  finalMsg = CONST.TRIAGE_WEEKLY_MSG_TEMPLATE.format(*msg_values)
  try:
    slack.post_message(
      finalMsg,
      attachments=CONST.TRIAGE_WEEKLY_MSG_ATTACHMENTS)
  except Exception as e:
    print("Failed to post weekly triage message: {}".format(repr(e)))
    return False
  return True
