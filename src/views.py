from src import app
from src.helpers import slack

from flask import request, Response, jsonify
import sys

@app.route("/triagemgmt/<meth>", methods=["POST"])
def main(meth=None):
  s = slack.SlackApi()
  requestJson = request.get_json()
  # Handle verification
  if (requestJson):
    if requestJson.get('type', None) == "url_verification":
      return s.handle_verification(requestJson)
    
  print(request.data)
  print(request.form)
  print(request.get_json())

  return jsonify({"Answer":"None"})
