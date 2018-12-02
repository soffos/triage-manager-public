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
    SLACK_API_BASE = config.get("slack", 'api_base')
  except Exception as e:
    print("Error importing Slack configuration: {}".format(repr(e)))

  try:
    DB_TYPE = config.get("db", 'type')
    DB_USER = config.get("db", 'user')
    DB_PASS = config.get("db", 'pass')
    if DB_PASS != "":
      DB_PASS = ":"+DB_PASS
    
    DB_HOST = config.get("db", 'host')
    DB_PORT = config.get("db", 'port')
    DB_NAME = config.get("db", 'name')
    SQLALCHEMY_DATABASE_URI = "{0}://{1}{2}@{3}:{4}/{5}".format(
                                DB_TYPE,
                                DB_USER,
                                DB_PASS,
                                DB_HOST,
                                str(DB_PORT),
                                DB_NAME
                              )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
  except Exception as e:
    print("Error importing DB configuration: {}".format(repr(e)))

class Production(Config):
  ENV = "Production"
  DEBUG = False
  TESTING = False

class Development(Config):
  ENV = "Development"
  DEBUG = True
  TESTING = True
