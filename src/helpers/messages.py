from src import db, models
import src.helpers.constants as CONST
from src.helpers import data_access

import requests

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
  try:
    r = slack.post_message(
      get_weekly_message(),
      attachments=CONST.TRIAGE_WEEKLY_MSG_ATTACHMENTS
    )
  except Exception as e:
    print("Failed to post weekly triage message: {}".format(repr(e)))
    return False
  # Save ts to db for later updates
  newMessage = models.Messages(slack_ts=r.get('ts', ""))
  db.session.add(newMessage)
  db.session.commit()
  return True

def update_weekly_message(slack):
  try:
    r = slack.update_message(
      get_weekly_message(False),
      data_access.get_target_ts(),
      attachments=CONST.TRIAGE_WEEKLY_MSG_ATTACHMENTS
    )
  except Exception as e:
    print("Failed to update weekly triage message: {}".format(repr(e)))
    raise
    return False
  return True

def update_ephemeral(slack, data):
  try:
    slack.post_ephemeral_message("Thanks for signing up!", data['user']['id'], response_url=data['response_url'], attachments=[])
  except Exception as e:
    print("Failed to update ephemeral: {}".format(repr(e)))


def get_weekly_message(initial_message=True):
  reservations = data_access.get_triage_reservations(initial_message)
  msg_values = []
  for dow in ["m","t","w","h","f"]:
    for t in range(1,4):
      msg_values.extend(reservations[dow][str(t)])
  return CONST.TRIAGE_WEEKLY_MSG_TEMPLATE.format(*msg_values)

def get_ephemeral_timeslot_attachments(day_of_week):
  print(day_of_week)
  tmp = CONST.TRIAGE_TIMESLOT_ATTACHMENTS[0]
  for idx,d in enumerate(tmp['actions']):
    tmp['actions'][idx]['name'] = d['name'].format(day_of_week)
  return [tmp]
