from src import app, models
from sqlalchemy import and_
from src.helpers.calendar import send_invite_by_epoch_day_slot
from src.helpers.slack import SlackApi

def ensure_calendar_accuracy():
  # Slck API
  s = SlackApi()
  # First get relevant epoch
  targetTs = models.Messages.query.order_by(models.Messages.slack_ts.desc())[0].slack_ts
  reservations = models.Reservation.query.filter(models.Reservation.target_slack_ts==str(targetTs)).all()

  # De-duplicate. If a user has signed up for 1-3, sign them up for the full block
  resUsers = {}
  dedupRes = []
  # collect reservation usernames
  for res in reservations:
    if res.uid not in resUsers.keys():
      resUsers[res.uid] = res
  # collect reservations categorized by days, per user
  for resUser in resUsers.keys():
    dedupDict = {}
    resUserInfo = s.get_user_info(resUser)
    resList = models.Reservation.query.filter(and_(models.Reservation.target_slack_ts==str(targetTs),models.Reservation.name==resUsers[resUser].name)).all()
    for res in resList:
      if res.dow not in dedupDict.keys():
        dedupDict[res.dow] = [res.timeslot]
      else:
        dedupDict[res.dow] += res.timeslot
    # Add a 4th item to signify all blocks
    for key,value in dedupDict.items():
      print(resUser, key, value)
      if len(value)==3:
        send_invite_by_epoch_day_slot(resUserInfo['user']['profile']['email'], float(targetTs), key, 3)
      else:
        for ts in value:
          send_invite_by_epoch_day_slot(resUserInfo['user']['profile']['email'], float(targetTs), key, int(ts)-1)
