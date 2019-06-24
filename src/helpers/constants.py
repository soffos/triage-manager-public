TRIAGE_WEEKLY_MSG_TEMPLATE = "<!here> If you have the cycles, please sign up for a triage block or two for next week. Each day comprises three one-hour triage blocks from 12:00 - 3:00 PM, with a target of double coverage for every triage block.\nWhen starting your triage block, remember to set notifications on the #triage_tickets channel so you will be notified as cases come in. Also refer to the Wiki Page: https://wiki.corp.tanium.com/display/TT/Starting+your+Triage+Block \nCurrent schedule:```M - {} | {} | {}\nT - {} | {} | {}\nW - {} | {} | {}\nH - {} | {} | {}\nF - {} | {} | {}```"
TRIAGE_WEEKLY_MSG_ATTACHMENTS = [
  {
    "fallback": "Choose a day or three",
    "title": "Choose a day or three",
    "callback_id": "signup_dow_selection",
    "color": "#3AA3E3",
    "attachment_type": "default",
    "actions": [
      {
        "name": "monday",
        "text": "Monday",
        "type": "button",
        "value": "mon"
      },
      {
        "name": "tuesday",
        "text": "Tuesday",
        "type": "button",
        "value": "tue"
      },
      {
        "name": "wednesday",
        "text": "Wednesday",
        "type": "button",
        "value": "wed"
      },
      {
        "name": "thursday",
        "text": "Thursday",
        "type": "button",
        "value": "thu"
      },
      {
        "name": "friday",
        "text": "Friday",
        "type": "button",
        "value": "fri"
      }
    ]
  }
]
#TRIAGE_WEEKLY_MSG_TEMPLATE = "<!here> If you have the cycles, please sign up for a triage block or two for next week. Each day comprises three one-hour triage blocks, with a target of double coverage for every triage block.\nCurrent schedule:```M - Presidents' Day\nT - {} | {} | {}\nW - {} | {} | {}\nH - {} | {} | {}\nF - {} | {} | {}```"
#TRIAGE_WEEKLY_MSG_ATTACHMENTS = [
#  {
#    "fallback": "Choose a day or three",
#    "title": "Choose a day or three",
#    "callback_id": "signup_dow_selection",
#    "color": "#3AA3E3",
#    "attachment_type": "default",
#    "actions": [
#      {
#        "name": "tuesday",
#        "text": "Tuesday",
#        "type": "button",
#        "value": "tue"
#      },
#      {
#        "name": "wednesday",
#        "text": "Wednesday",
#        "type": "button",
#        "value": "wed"
#      },
#      {
#        "name": "thursday",
#        "text": "Thursday",
#        "type": "button",
#        "value": "thu"
#      },
#      {
#        "name": "friday",
#        "text": "Friday",
#        "type": "button",
#        "value": "fri"
#      }
#    ]
#  }
#]
TRIAGE_TIMESLOT_ATTACHMENTS = [
  {
    "fallback": "Choose a time slot:",
    "title": "Choose a time slot:",
    "callback_id": "signup_ts_selection",
    "color": "#3AA3E3",
    "attachment_type": "default",
    "actions": [
      {
        "name": "{}1",
        "text": "12:00 P.M. - 1:00 P.M.",
        "type": "button",
        "value": "1",
      },
      {
        "name": "{}2",
        "text": "1:00 P.M. - 2:00 P.M.",
        "type": "button",
        "value": "2",
      },
      {
        "name": "{}3",
        "text": "2:00 P.M. - 3:00 P.M.",
        "type": "button",
        "value": "3",
      },
      {
        "name": "{}4",
        "text": "All blocks",
        "type": "button",
        "value": "4",
      },
      {
        "name": "{}5",
        "text": "Remove me",
        "type": "button",
        "style": "danger",
        "value": "5"
      }
    ]
  }
]
