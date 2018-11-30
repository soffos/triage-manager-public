from src import app
from src.helpers import slack

from flask import request, Response, jsonify

@app.route("/triagemgmt/<method>")
def main(method=None):
  print(request.form)
  print(request.get_json())
  return jsonify({"Answer":"None"})
