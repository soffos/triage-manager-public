from src import db, models
import src.helpers.constants as CONST
from src.helpers import data_access

import requests
import copy

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
  import pprint
  pp = pprint.PrettyPrinter()
  pp.pprint(r)
  # Save ts to db for later updates
  newMessage = models.Messages(slack_ts=r.get('ts', ""))
  db.session.add(newMessage)
  db.session.commit()
  return True

def update_weekly_message(slack, target_ts):
  try:
    r = slack.update_message(
      get_weekly_message(False, target_ts),
      data_access.get_target_ts()
    )
  except Exception as e:
    print("Failed to update weekly triage message: {}".format(repr(e)))
    raise
    return False
  return True

def update_ephemeral(slack, data):
  try:
    slack.post_ephemeral_message("Sign-up received!", data['user']['id'], response_url=data['response_url'], attachments=[])
  except Exception as e:
    print("Failed to update ephemeral: {}".format(repr(e)))


def get_weekly_message(initial_message=True, target_ts=None):
  reservations = data_access.get_triage_reservations(initial_message, target_ts)
  msg_values = []
  for dow in ["mon","tue","wed","thu","fri"]:
    for t in range(1,4):
      tsNames = reservations[dow][str(t)]
      msg_values.append(",".join(tsNames))
      #msg_values.extend(reservations[dow][str(t)])
  weekly_msg_template = copy.deepcopy(CONST.TRIAGE_WEEKLY_MSG_TEMPLATE)
  return weekly_msg_template.format(*msg_values)

#def get_weekly_message(initial_message=True, target_ts=None):
#  reservations = data_access.get_triage_reservations(initial_message, target_ts)
#  msg_values = []
#  for dow in ["tue","wed","thu","fri"]:
#    for t in range(1,4):
#      tsNames = reservations[dow][str(t)]
#      msg_values.append(",".join(tsNames))
#      #msg_values.extend(reservations[dow][str(t)])
#  weekly_msg_template = copy.deepcopy(CONST.TRIAGE_WEEKLY_MSG_TEMPLATE)
#  return weekly_msg_template.format(*msg_values)

def get_ephemeral_timeslot_attachments(day_of_week, message_ts):
  tmp = copy.deepcopy(CONST.TRIAGE_TIMESLOT_ATTACHMENTS[0])
  for idx,d in enumerate(tmp['actions']):
    tmp['actions'][idx]['name'] = d['name'].format(day_of_week)
    tmp['actions'][idx]['value'] = str(message_ts)
  return [tmp]
