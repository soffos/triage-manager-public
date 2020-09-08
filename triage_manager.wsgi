activate_this = "/srv/triage-manager/venv/bin/activate_this.py"
with open(activate_this) as f:
  exec(f.read(), dict(__file__=activate_this))

import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/html/triage-manager")
print(sys.path)
from src import app as application
