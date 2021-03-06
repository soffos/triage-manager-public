from src import app, db, models
from src.helpers import slack, constants, messages, calendar, data_access, reporting
from src.helpers.decorators import validate_slack_message

from flask import request, Response, jsonify
import sys
import json

def handle_day_selection(slack, data):
  messageTs = data.get('message_ts', 0)
  slack.post_ephemeral_message(
    "Pick a time slot for {}:".format(data['actions'][0]['name'].capitalize()),
    data.get('user', {}).get('id', ""),
    attachments=messages.get_ephemeral_timeslot_attachments(data['actions'][0]['value'],messageTs)
  )
  # Should return to wipe the message
  return ('',200)

def handle_make_reservation(slack, data):
  actionContent = data['actions'][0]
  targetTs = actionContent.get('value', 0)

  data_access.save_triage_reservation(data, targetTs)
  messages.update_ephemeral(slack, data)
  messages.update_weekly_message(slack, targetTs)
  data['targetTs'] = targetTs
  # Send calendar invite
  handle_send_calendar_invite(slack, data, actionContent)
  return ('',200)

def handle_send_calendar_invite(slack, data, meta):
  try:
    userInfo = slack.get_user_info(data['user']['id'])
    userEmail = userInfo['user']['profile']['email']
    # Need to ensure ephemeral button 'value' is original message ts for granularity
    day = meta['name'][:3]
    slot = int(meta['name'][-1:])
    if slot == 5:
      calendar.remove_invitation_by_epoch_day_slot(userEmail, float(data['targetTs']), day, None)
    else:
      slot = slot - 1 if slot < 4 else None
      calendar.send_invite_by_epoch_day_slot(userEmail, float(data['targetTs']), day, slot)
  except Exception as e:
    # Don't fail just due to calendar failure
    print("Failed to send calendar invite: {}".format(repr(e)))
  return False

def handle_get_leaderboard(slack, data):
  messageTs = data['message']['ts']
  if data.get('actions', [{}])[0].get('value', "") == "rep":
    slack.post_ephemeral_message(
      "Check out our leading triagers!\n{}\n>`Leaderboard captures 13 most recent triage rosters`".format(reporting.run_participation_report()),
      data.get('user', {}).get('id', "")
    )
  else:
    slack.post_ephemeral_message(
      "Pick a time slot for {}:".format(data['user']['name'].capitalize()),
      data.get('user', {}).get('id', ""),
      attachments=messages.get_ephemeral_timeslot_attachments(data['actions'][0]['value'],messageTs)
    )
  return ('',200)

@app.route("/triagemgmt/<meth>", methods=["POST"])
@validate_slack_message
def main(meth=None):
  s = slack.SlackApi()
  requestJson = request.get_json()
  # Handle verification
  if requestJson:
    if requestJson.get('type', None) == "url_verification":
      return s.handle_verification(requestJson)

  if request.form:
    requestDict = json.loads(request.form.to_dict().get('payload', request.form.to_dict()))

  if requestDict:
    # Handle triage day selection
    if requestDict.get('callback_id', None) == "signup_dow_selection":
      return handle_day_selection

    elif requestDict.get('callback_id', None) == "signup_ts_selection":
      # Add reservation(s) to db and update slack message
      return handle_make_reservation(s, requestDict)
      
    elif requestDict.get('type', "") == "block_actions":
      return handle_get_leaderboard(s, requestDict)

    print("requestDict:");print(requestDict)
  print("Request.data: {}".format(request.data))
  print("Request.form: {}".format(request.form))
  print("Dict form of Request.form: {}".format(request.form.to_dict()))
  print("Request.get_json(): {}".format(request.get_json()))

  return ('',204)

@app.route('/', methods=['GET','POST'])
def index():
  print("Received invalid request: /")
  return ('',500)

@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
  print("Received invalid request: {}".format(str(path)))
  return ('',500)
