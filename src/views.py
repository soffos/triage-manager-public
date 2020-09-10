from src import app, db, models
from src.helpers import slack, constants, messages, calendar, data_access, reporting
from src.helpers.decorators import validate_slack_message

from flask import request, Response, jsonify
import sys
import json

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
      messageTs = requestDict.get('message_ts', 0)
      s.post_ephemeral_message(
        "Pick a time slot for {}:".format(requestDict['actions'][0]['name'].capitalize()),
        requestDict.get('user', {}).get('id', ""),
        attachments=messages.get_ephemeral_timeslot_attachments(requestDict['actions'][0]['value'],messageTs)
      )
      return ('',200)
      # Should return something to wipe the message
      # return "None or something"
    elif requestDict.get('callback_id', None) == "signup_ts_selection":
      # Add reservation(s) to db and update slack message
      actionContent = requestDict['actions'][0]
      targetTs = actionContent.get('value', 0)
      data_access.save_triage_reservation(requestDict, targetTs)
      messages.update_ephemeral(s, requestDict)
      messages.update_weekly_message(s, targetTs)
      # Send calendar invite
      try:
        userInfo = s.get_user_info(requestDict['user']['id'])
        userEmail = userInfo['user']['profile']['email']
        # Need to ensure ephemeral button 'value' is original message ts for granularity
        day = actionContent['name'][:3]
        slot = int(actionContent['name'][-1:])
        if slot == 5:
          calendar.remove_invitation_by_epoch_day_slot(userEmail, float(targetTs), day, None)
        else:
          slot = slot - 1 if slot < 4 else None
          calendar.send_invite_by_epoch_day_slot(userEmail, float(targetTs), day, slot)
      except Exception as e:
        print("Failed to send calendar invite: {}".format(repr(e)))
      return ('',200)
    elif requestDict.get('type', "") == "block_actions":
      #import pprint;pprint.PrettyPrinter().pprint(requestDict);
      messageTs = requestDict['message']['ts']
      if requestDict.get('actions', [{}])[0].get('value', "") == "rep":
        s.post_ephemeral_message(
          "Check out our leading triagers!\n{}\n>`Leaderboard captures 13 most recent triage rosters`".format(reporting.run_participation_report()),
          requestDict.get('user', {}).get('id', "")
        )
      else:
        s.post_ephemeral_message(
          "Pick a time slot for {}:".format(requestDict['user']['name'].capitalize()),
          requestDict.get('user', {}).get('id', ""),
          attachments=messages.get_ephemeral_timeslot_attachments(requestDict['actions'][0]['value'],messageTs)
        )
      return ('',200)
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
