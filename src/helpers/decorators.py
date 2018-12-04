from src import app

from flask import request
from functools import wraps
import inspect
import hmac
import hashlib
import urllib.parse
import json
import time

def ensure_dict(func):
  def ensure(*args, **kwargs):
    try:
      data = args[inspect.getargspec(func)[0].index('data')]
    except NameError:
      print("No `data` variable passed")
      raise
    if not isinstance(data, dict):
      raise TypeError("`data` variable is not a dict")
    else:
      return func(*args, **kwargs)
  return ensure

def validate_slack_message(func):
  @wraps(func)
  def validate(*args, **kwargs):
    # Pull request headers
    slackSig = request.headers.get('X-Slack-Signature')
    slackTs = request.headers.get('X-Slack-Request-Timestamp')
    # No MITM for me
    if abs(time.time() - float(slackTs)) > 60 * 5:
      raise ValueError("Slack request timestamp differs by > 5 minutes from local time.")
    # Form basestring
    bs = "{}:{}:{}".format("v0", slackTs, str(request.get_data(), 'utf-8'))
    # Compute signature
    compSig = "v0={}".format(hmac.new(app.config['SLACK_SIGNING_SECRET'].encode(), msg=bs.encode(), digestmod=hashlib.sha256).hexdigest())
    # Compare
    if not hmac.compare_digest(slackSig, compSig):
      raise ValueError("Slack signature did not match computed signature: bs: {},  {} / {}".format(bs, slackSig, compSig))
    else:
      return func(*args, **kwargs)
  return validate
