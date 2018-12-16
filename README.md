# triage-manager

triage-manager is designed to make signing up for weekly triage a breeze. This manages a text-based schedule in a Slack channel, along with invitations to a shared Triage calendar.

### Tech

* Python-Flask
* Python-SQLAlchemy
* Slack API
* Google Calendar API
* MySQL

### Installation

triage-manager requires Python 3.7+ to run properly.

A sample config.ini has been provided to outline the required information for the app to run.

Create a virtualenv for app dependencies, install from the provided `requirements.txt`
```
cd git-project-tld
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
```

Bootstrap the DB:
```
. venv/bin/activate
./db_create.py
```

For the app to function to its fullest, Google API credentials are required. Run the below commands and follow the authorization flow:
```
. venv/bin/activate
./gcal_authorization.py
```
The above is only required during initial setup, credentials will be stored for future use.

Currently the app is only designed to run via the test server:
```
. venv/bin/activate
./run.py
```

