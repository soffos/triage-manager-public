from src import app

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file

import logging

class GoogleApi():
  def __init__(self, **kwargs):
    logging.getLogger('googleapiclient.discovery').setLevel(logging.ERROR)
    self.API_BASE = kwargs.get('API_BASE', app.config['GCAL_API_BASE'])
    credStore = file.Storage("{}/conf/gcal_token.json".format(app.config['BASEDIR']))
    self.credentials = credStore.get()

  def list_calendar_events_in_range(self, time_min, time_max):
    service = self._get_authorized_service("calendar")
    pageToken = None
    ret_events = []
    while True:
      events = service.events().list(
        calendarId=app.config['GCAL_CALENDAR_ID'],
        pageToken=pageToken,
        singleEvents=True,
        timeMin=time_min,
        timeMax=time_max
      ).execute()
      for event in events['items']:
        print(event['summary'])
        ret_events.append(event)
      pageToken = events.get('nextPageToken', None)
      if not pageToken:
        break
    return ret_events

  def _get_authorized_service(self, target_svc):
    return build(target_svc, 'v3', http=self.credentials.authorize(Http()), cache_discovery=False)
