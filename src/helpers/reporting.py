from src.models import Reservation
from src.helpers import constants

import datetime
import pprint

def datetime_to_epoch(dt):
  return dt.strftime('%s')

def get_participation_dict(time_range=None):
  # Dict to hold participation data
  pDict = {}
  # Get all rows based on time_range
  if time_range is None:
    # If no specified range, grab last 13 rosters
    tgtTsList = Reservation.query.order_by(Reservation.target_slack_ts.asc()).with_entities(Reservation.target_slack_ts).distinct()[-13:]
    reservRows = Reservation.query.filter(Reservation.target_slack_ts.in_([str(t.target_slack_ts) for t in tgtTsList])).order_by(Reservation.target_slack_ts.desc())
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
    for user in usersDict.keys():
      avg = 0
      for ts, userDict in pDict.items():
        numHrs = len(userDict.get(user, []))
        avg += numHrs
        if numHrs < target_ratio and include_missed_weeks:
          usersDict[user]['missed_weeks'].append({ts: numHrs})
      usersDict[user]['total'] = avg
      usersDict[user]['average'] = float(avg)/float(totalWeeks)
      if usersDict[user]['average'] >= target_ratio:
        usersDict[user]['compliant'] = True

  pprint.PrettyPrinter().pprint(usersDict)
  return usersDict

def run_participation_report():
  print("Running participation report...")
  # How many times a user must participate per week
  participTargetRatio = 2.0
  tgtUsers = []
  tgtRange = None#(datetime.datetime.now() - datetime.timedelta(days=90), datetime.datetime.now())
 
  paddingAlpha = "{}"; paddingNum = "{}"; 
  reportListified = []
  report = create_participation_report(participTargetRatio, time_range=tgtRange, users=tgtUsers)
  for k,v in report.items():
    rO = v; rO['name'] = k
    reportListified.append(rO)
  outMsg = ""
  nrmlLn = 13#8
  highTot = 0
  highAvg = 0
  for o in reportListified:
    nrmlLn = nrmlLn if len(o['name'])+2 <= nrmlLn else len(o['name'])+2
  for obj in sorted(reportListified, key= lambda i: i['total'], reverse=True):
    if obj['average'] < participTargetRatio:
      continue
    paddingAlpha = "{:<" + str(nrmlLn) + "}"
    paddingNum = "{:^" + str(nrmlLn) + "s}"
    objName = paddingAlpha.format(obj.get('name', "Error"))
    objAvgNum = obj.get('average', 0)
    objAvg = paddingNum.format("{:.2f}".format(objAvgNum))
    objTotNum = obj.get('total', 0)
    objTot = paddingNum.format(str(objTotNum))

    outMsg += constants.TRIAGE_LEADERBOARD_TEMPLATE.format(objName, objAvg, objTot) + "\n"

  nrmlHeaders = constants.TRIAGE_LEADERBOARD_TEMPLATE_HEADERS
  nrmlHeaders = "|".join([paddingNum.format(x) for x in nrmlHeaders.split('|')])
  nrmlHeaders = nrmlHeaders[:nrmlHeaders.find('|')] + " " + nrmlHeaders[nrmlHeaders.find('|')+1:]

  if outMsg.strip() == "":
    return "_*No one qualified.*_"
  else:
    return "```" + nrmlHeaders + "\n" + outMsg + "```"
