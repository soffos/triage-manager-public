# Need a report that shows consistent triage participation, 2 triage blocks per week minimum
# Select all reservations, sorted by slack_message_ts in chrono order
# Keep running tally of every user
# Each user should have 2 distinct dow-timeslot combinations for each slack_message_ts
# Report user, average participation (hrs/wk over a long period) and under-performing weeks if under threshold (datetime)
from src.models import Reservation

import datetime
import pprint

def datetime_to_epoch(dt):
  return dt.strftime('%s')

def get_participation_dict(time_range=None):
  # Dict to hold participation data
  pDict = {}
  # Get all rows based on time_range
  if time_range is None:
    reservRows = Reservation.query.order_by(Reservation.target_slack_ts.asc())
  else:
    start_ts, end_ts = (str(datetime_to_epoch(time_range[0])), str(datetime_to_epoch(time_range[1])))
    reservRows = Reservation.query.filter((Reservation.target_slack_ts >= start_ts) & (Reservation.target_slack_ts <= end_ts)).order_by(Reservation.target_slack_ts.asc())
  # For each target_slack_ts
  for res in reservRows:
    if res.target_slack_ts not in pDict:
      pDict[res.target_slack_ts] = {}
    if res.name not in pDict[res.target_slack_ts]:
      pDict[res.target_slack_ts][res.name] = []
    slotTuple = (res.dow,res.timeslot)
    if slotTuple not in pDict[res.target_slack_ts][res.name]:
      pDict[res.target_slack_ts][res.name].append(slotTuple)
  return pDict

def create_participation_report(target_ratio, time_range=None, users=[], include_missed_weeks=False):
  pDict = get_participation_dict(time_range)
  usersDict = {k.name:{"compliant": False, "average": 0, "missed_weeks": []} for k in Reservation.query.with_entities(Reservation.name).distinct() if (len(users)==0 or k.name in users)}
  # Calculate average participation slots per week for each user
  totalWeeks = len(pDict.keys())
  if totalWeeks != 0:
    for user in usersDict:
      avg = 0
      for ts, userDict in pDict.items():
        numHrs = len(userDict.get(user, []))
        avg += numHrs
        if numHrs < target_ratio and include_missed_weeks:
          usersDict[user]['missed_weeks'].append({ts: numHrs})
      usersDict[user]['average'] = float(avg)/float(totalWeeks)
      if usersDict[user]['average'] >= target_ratio:
        usersDict[user]['compliant'] = True

  pprint.PrettyPrinter().pprint(usersDict)
  return usersDict

if __name__=="__main__":
  print("Running participation report...")
  # How many times a user must participate per week
  participTargetRatio = 2.0
  tgtUsers = ["add users here"]
  tgtRange = (datetime.datetime.now() - datetime.timedelta(days=90), datetime.datetime.now()) 

  create_participation_report(participTargetRatio, time_range=tgtRange, users=tgtUsers)
