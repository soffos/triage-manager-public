from src import app

import json
from googleapiclient.discovery import build
import google.oauth2.credentials
from httplib2 import Http
from oauth2client import file

import logging

class MemCache():
  _CACHE = {}
  def get(self, url):
    return MemCache._CACHE.get(url)
  def set(self, url, content):
    MemCache._CACHE[url] = content

class GoogleApi():
  def __init__(self, **kwargs):
    logging.getLogger('googleapiclient.discovery').setLevel(logging.ERROR)
    with open("{}/conf/gcal_token.json".format(app.config['BASEDIR'])) as f:
      creds = json.load(f)

    self.credentials = google.oauth2.credentials.Credentials(**creds) 
    print("Set credentials to {}".format(self.credentials))

  def list_calendar_events_in_range(self, time_min, time_max):
    service = self.__get_authorized_service("calendar")
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
        ret_events.append(event)
      pageToken = events.get('nextPageToken', None)
      if not pageToken:
        break
    return ret_events

  def update_calendar_event(self, calendar_id, event):
    service = self.__get_authorized_service("calendar")
    return service.events().update(calendarId=calendar_id, eventId=event['id'], body=event).execute()

  def __get_authorized_service(self, target_svc):
    return build(target_svc, 'v3', credentials=self.credentials, cache=MemCache())
    #return build(target_svc, 'v3', http=self.credentials.authorize(Http()), cache_discovery=False)
