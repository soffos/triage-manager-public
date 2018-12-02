from src import app
from src.helpers.decorators import *

from flask import jsonify

import requests
import json

class SlackApi():
  def __init__(self, **kwargs):
    self.API_BASE = kwargs.get('API_BASE', app.config['SLACK_API_BASE'])
    self.API_TOKEN = kwargs.get('API_TOKEN', app.config['SLACK_ACCESS_TOKEN'])
    self.CHANNEL_ID = kwargs.get('CHANNEL_ID', app.config.get('SLACK_CHANNEL_ID'))
    self.SIGNING_SECRET = kwargs.get('SIGNING_SECRET', app.config.get('SLACK_SIGNING_SECRET'))

  @ensure_dict
  def handle_verification(self, data):
    resp = data.get('challenge', None)
    if resp:
      return jsonify({'challenge': resp}), 200
    return jsonify({}), 400

  def post_message(self, text, **kwargs):
    targetUrl = "{}{}".format(self.API_BASE, "chat.postMessage")
    payload = {
      'channel': self.CHANNEL_ID,
      'text': text,
      'as_user': kwargs.get('as_user', False),
      'attachments': kwargs.get('attachments', [])
    }
    r = requests.post(targetUrl,
      data=json.dumps(payload),
      headers={'Content-type': 'application/json',
               'Authorization': "Bearer {}".format(self.API_TOKEN)}
    )
    return r.json()

  def post_ephemeral_message(self, text, target_user_id, **kwargs):
    targetUrl = "{}{}".format(self.API_BASE, "chat.postEphemeral")
    payload = {
      'channel': kwargs.get('channel_id', self.CHANNEL_ID),
      'text': text,
      'as_user': kwargs.get('as_user', False),
      'attachments': kwargs.get('attachments', []),
      'user': target_user_id
    }
    r = requests.post(targetUrl,
      data=json.dumps(payload),
      headers={'Content-Type': "application/json",
               'Authorization': "Bearer {}".format(self.API_TOKEN)}
    )
    return r.json()
