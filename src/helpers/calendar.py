from src.helpers.google import GoogleApi

from datetime import datetime, timedelta

def send_invite_by_epoch_day_slot(epoch, day, slot=None):
  # If slot is None, all-day invite
  # First need to grab events
  # Then determine target slot
  # Finally send invite
  pass

def get_event_length_hours(event):
  start = event.get('start', {})
  end = event.get('end', {})
  startDt = datetime.fromisoformat(start.get('dateTime', ""))
  endDt = datetime.fromisoformat(end.get('dateTime', ""))
  diff = end_dt - start_dt
  return diff.seconds / 3600

def get_gcal_events_by_epoch(epoch):
  return GoogleApi().list_calendar_events_in_range(
    get_bound_of_week_from_epoch(epoch),
    get_bound_of_week_from_epoch(epoch, True)
  )

def get_bound_of_week_from_epoch(epoch, end=False):
  current = convert_epoch_to_datetime(epoch)
  start = current - timedelta(days=current.weekday())
  if not end:
    return start.replace(hour=0, minute=0).isoformat() + 'Z'
  return (start.replace(hour=23, minute=59) + timedelta(days=6)).isoformat() + 'Z'

def convert_epoch_to_datetime(epoch):
  return datetime.utcfromtimestamp(epoch)
