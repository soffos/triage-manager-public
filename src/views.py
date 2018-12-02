from src import app
from src.helpers import slack, constants

from flask import request, Response, jsonify
import sys
import json

@app.route("/triagemgmt/<meth>", methods=["POST"])
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
    # Handle returns from button clicks
    if requestDict.get('callback_id', None) == "signup_dow_selection":
      s.post_ephemeral_message(
        "Pick a time slot:",
        requestDict.get('user', {}).get('id', ""),
        attachments=constants.TRIAGE_TIMESLOT_ATTACHMENTS
      )
  print("Request.data: {}".format(request.data))
  print("Request.form: {}".format(request.form))
  print("Dict form of Request.form: {}".format(request.form.to_dict()))
  print("Request.get_json(): {}".format(request.get_json()))

  return jsonify({"Answer":"None"})
