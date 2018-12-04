from src import app, db, models
from src.helpers import slack, constants, messages, data_access
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
    requestDict = json.loads(request.form.to_dict().get('payload', None))

  if requestDict:
    # Handle triage day selection
    if requestDict.get('callback_id', None) == "signup_dow_selection":
      s.post_ephemeral_message(
        "Pick a time slot for {}:".format(requestDict['actions'][0]['name'].capitalize()),
        requestDict.get('user', {}).get('id', ""),
        attachments=messages.get_ephemeral_timeslot_attachments(requestDict['actions'][0]['value'])
      )
      return ('',200)
      # Should return something to wipe the message
      # return "None or something"
    elif requestDict.get('callback_id', None) == "signup_ts_selection":
      # Add reservation(s) to db and update slack message
      data_access.save_triage_reservation(requestDict)
      messages.update_ephemeral(s, requestDict)
      messages.update_weekly_message(s)
      # Also return an update to the ephemeral message?
      return ('',200)
  print("Request.data: {}".format(request.data))
  print("Request.form: {}".format(request.form))
  print("Dict form of Request.form: {}".format(request.form.to_dict()))
  print("Request.get_json(): {}".format(request.get_json()))

  return ('',204)
