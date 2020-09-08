from src import app
from src.helpers.google import GoogleApi

from datetime import datetime, timedelta

def send_invite_by_epoch_day_slot(email, epoch, day, slot=None):
  gapi = GoogleApi()
  # If slot is None, all-day invite
  if slot is None:
    slot=3
  # First need to grab events
  allEvents = get_gcal_events_by_epoch(epoch)
  allEvents = sort_events_by_start_date(allEvents)
  # Then determine target slot
  dow = ["mon","tue","wed","thu","fri"]
  dayIdx = dow.index(day.lower())
  relEvents = allEvents[dayIdx*4:dayIdx*4+4]
  for idx,event in enumerate(relEvents):
    if get_event_length_hours(event) > 1:
      popIdx = idx
      break
  p = relEvents.pop(popIdx)
  relEvents.append(p)
  # Finally send invite
  targetEvent = relEvents[slot]
  currAttendees = targetEvent.get('attendees', [])
  attendeeExists = False
  for existing in currAttendees:
    if existing.get('email', '') == email:
      attendeeExists = True
  if not attendeeExists:
    currAttendees.append({'email': email})
    targetEvent['attendees'] = currAttendees
    updatedEvent = gapi.update_calendar_event(app.config['GCAL_CALENDAR_ID'], targetEvent)
    return updatedEvent
  return targetEvent

def remove_invitation_by_epoch_day_slot(email, epoch, day, slot=None):
  gapi = GoogleApi()
  # First need to retrieve events
  allEvents = get_gcal_events_by_epoch(epoch)
  allEvents = sort_events_by_start_date(allEvents)
  # Then determine target slot
  dow = ["mon","tue","wed","thu","fri"]
  dayIdx = dow.index(day.lower())
  relEvents = allEvents[dayIdx*4:dayIdx*4+4]
  for idx,event in enumerate(relEvents):
    if get_event_length_hours(event) > 1:
      popIdx = idx
      break
  p = relEvents.pop(popIdx)
  relEvents.append(p)
  # Finally delete attendee
  for eventIdx,event in enumerate(relEvents):
    targetEvent = relEvents[eventIdx]
    currAttendees = targetEvent.get('attendees', [])
    deleteIdx = None
    for idx,attend in enumerate(currAttendees):
      eml = attend.get('email', None)
      if eml is not None:
        deleteIdx = idx
    if deleteIdx is not None:
      currAttendees.pop(deleteIdx)
      targetEvent['attendees'] = currAttendees
      updatedEvent = gapi.update_calendar_event(app.config['GCAL_CALENDAR_ID'], targetEvent)
  return True

def sort_events_by_start_date(events):
  retEvents = []
  sortList = []
  for event in events:
    startDate = event['start']['dateTime']
    sortList.append({'start': startDate, 'event': event})
  for event in sorted(sortList, key=lambda k: k['start']):
    retEvents.append(event['event'])
  return retEvents

def get_event_length_hours(event):
  start = event.get('start', {})
  end = event.get('end', {})
  startDt = datetime.fromisoformat(start.get('dateTime', ""))
  endDt = datetime.fromisoformat(end.get('dateTime', ""))
  diff = endDt - startDt
  return diff.seconds / 3600

def get_gcal_events_by_epoch(epoch):
  return GoogleApi().list_calendar_events_in_range(
    get_bound_of_next_week_from_epoch(epoch),
    get_bound_of_next_week_from_epoch(epoch, True)
  )

def get_bound_of_next_week_from_epoch(epoch, end=False):
  current = convert_epoch_to_datetime(epoch)
  nw = current + timedelta(days=7)
  start = nw - timedelta(days=nw.weekday())
  if not end:
    return start.replace(hour=0, minute=0).isoformat() + 'Z'
  return (start.replace(hour=23, minute=59) + timedelta(days=6)).isoformat() + 'Z'

def convert_epoch_to_datetime(epoch):
  return datetime.utcfromtimestamp(epoch)
