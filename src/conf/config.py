import os
import random
import string
import configparser

class Config(object):
  def secret_generator(size=16, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
  SECRET_KEY = secret_generator()

  BASEDIR = os.path.abspath(os.path.dirname(__file__)).rsplit('/', 1)[0]

  config = configparser.ConfigParser()
  config.read(BASEDIR+"/conf/config.ini")
  if not config.sections():
    raise IOError("Must create config.ini in {}/conf/".format(BASEDIR))

  try:
    SLACK_APP_ID = config.get("slack", 'app_id')
    SLACK_BOT_UID = config.get("slack", 'bot_uid')
    SLACK_ACCESS_TOKEN = config.get("slack", 'access_token')
    SLACK_CHANNEL_ID = config.get("slack", 'channel_id')
    SLACK_SIGNING_SECRET = config.get("slack", 'signing_secret')
    SLACK_API_URL = config.get("slack", 'api_url')
  except Exception as e:
    print("Error importing Slack configuration: {}".format(repr(e)))

class Production(Config):
  DEBUG = False
  TESTING = False

class Development(Config):
  DEBUG = True
  TESTING = True
