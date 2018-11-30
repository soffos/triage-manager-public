import os
import random
import string
import configparser

class Config(object):
  def secret_generator(size=16, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
  SECRET_KEY = secret_generator()

  DEBUG = False
  TESTING = False
  BASEDIR = os.path.abspath(os.path.dirname(__file__)).rsplit('/', 1)[0]

  config = configparser.ConfigParser()
  config.read(BASEDIR+"/conf/config.ini")
  if not config.sections():
    raise IOError("Must create config.ini in {}/conf/".format(BASEDIR))

  try:
    # Import slack config
    pass
  except Exception as e:
    print("Error importing Slack configuration: {}".format(repr(e))

class Development(Config):
  DEBUG = True
  TESTING = False
