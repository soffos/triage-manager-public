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
    targetUrl = self.__get_api_url("chat.postMessage")
    payload = {
      'channel': kwargs.get('channel_id', self.CHANNEL_ID),
      'text': text,
      'as_user': kwargs.get('as_user', False),
      'attachments': kwargs.get('attachments', [])
    }
    return self.__make_api_request(targetUrl, payload)

  def post_ephemeral_message(self, text, target_user_id, **kwargs):
    targetUrl = kwargs.get('response_url', self.__get_api_url("chat.postEphemeral"))
    payload = {
      'channel': kwargs.get('channel_id', self.CHANNEL_ID),
      'text': text,
      'as_user': kwargs.get('as_user', False),
      'attachments': kwargs.get('attachments', []),
      'user': target_user_id
    }
    return self.__make_api_request(targetUrl, payload)

  def update_message(self, text, target_ts, **kwargs):
    targetUrl = self.__get_api_url("chat.update")
    payload = {
      'channel': kwargs.get('channel_id', self.CHANNEL_ID),
      'text': text,
      'as_user': kwargs.get('as_user', False),
      'attachments': kwargs.get('attachments', []),
      'ts': target_ts
    }
    return self.__make_api_request(targetUrl, payload)

  def __make_api_request(self, target_url, payload):
    if isinstance(payload, dict):
      payload = json.dumps(payload)
    elif not isinstance(payload, str):
      raise TypeError("Expected json string or dict")

    r = requests.post(target_url,
      data=payload,
      headers={'Content-Type': "application/json",
               'Authorization': "Bearer {}".format(self.API_TOKEN)}
    )
    return r.json()

  def __get_api_url(self, func):
    return "{}{}".format(self.API_BASE, func)
