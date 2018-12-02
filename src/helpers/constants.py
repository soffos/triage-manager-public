TRIAGE_WEEKLY_MSG_TEMPLATE = "<!here> If you have the cycles, please sign up for a triage block or two for next week. The goal is double coverage for every triage block.\nCurrent schedule:```M - {} / {} / {}\nT - {} / {} / {}\nW - {} / {} / {}\nH - {} / {} / {}\nF - {} / {} / {}```"
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
        "value": "m"
      },
      {
        "name": "tuesday",
        "text": "Tuesday",
        "type": "button",
        "value": "t"
      },
      {
        "name": "wednesday",
        "text": "Wednesday",
        "type": "button",
        "value": "w"
      },
      {
        "name": "thursday",
        "text": "Thursday",
        "type": "button",
        "value": "h"
      },
      {
        "name": "friday",
        "text": "Friday",
        "type": "button",
        "value": "f"
      }
    ]
  }
]
TRIAGE_TIMESLOT_ATTACHMENTS = [
  {
    "fallback": "Choose a time slot:",
    "title": "Choose a time slot:",
    "callback_id": "signup_ts_selection",
    "color": "#3AA3E3",
    "attachment_type": "default",
    "actions": [
      {
        "name": "1",
        "text": "12:00 P.M. - 1:00 P.M.",
        "type": "button",
        "value": "1"
      },
      {
        "name": "2",
        "text": "1:00 P.M. - 2:00 P.M.",
        "type": "button",
        "value": "2"
      },
      {
        "name": "3",
        "text": "2:00 P.M. - 3:00 P.M.",
        "type": "button",
        "value": "3"
      }
    ]
  }
]
