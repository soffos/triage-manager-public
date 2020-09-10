TRIAGE_WEEKLY_MSG_TEMPLATE = "<!here> If you have the cycles, please sign up for a triage block or two for next week. Each day's shift comprises three one-hour triage blocks from 12:00 - 3:00 PM. We need _at least_ double coverage for each block in order to ensure we consistently meet our SLAs.\nWhen starting your triage block, remember to set notifications on the <#C0L7DC8Q6|triage_tickets> channel so you will be notified as cases come in.\n<https://sites.google.com/tanium.com/tts/operations/triage|Triage G Site> | <#C0L7DC8Q6|triage_tickets> | <#C9MU2B4BA|triage_tickets-chat>\nCurrent schedule:```M - {} | {} | {}\nT - {} | {} | {}\nW - {} | {} | {}\nH - {} | {} | {}\nF - {} | {} | {}```"
TRIAGE_LEADERBOARD_TEMPLATE_HEADERS = " |Avg Hrs/Wk|Total"
TRIAGE_LEADERBOARD_TEMPLATE = "{}|{}|{}"
TRIAGE_WEEKLY_MSG_ATTACHMENTS_BLOCK = [
  { "color": "#3AA3E3",
    "blocks": [
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": "*Choose a day or three*"
        }
      },
      {
        "type": "actions",
        "block_id": "signup_dow_selection",
        "elements": [
          {
            "type": "button",
            "text": {
              "type": "plain_text",
              "text": "Monday",
              "emoji": True
            },
            "value": "mon"
          },
          {
            "type": "button",
            "text": {
              "type": "plain_text",
              "text": "Tuesday",
              "emoji": True
            },
            "value": "tue"
          },
          {
            "type": "button",
            "text": {
              "type": "plain_text",
              "text": "Wednesday",
              "emoji": True
            },
            "value": "wed"
          },
          {
            "type": "button",
            "text": {
              "type": "plain_text",
              "text": "Thursday",
              "emoji": True
            },
            "value": "thu"
          },
          {
            "type": "button",
            "text": {
              "type": "plain_text",
              "text": "Friday",
              "emoji": True
            },
            "value": "fri"
          },
          {
            "type": "button",
            "style": "primary",
            "text": {
              "type": "plain_text",
              "text": "Leaderboard",
              "emoji": True
            },
            "value": "rep",
          }
        ]
      }
    ]
  }
]
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
      },
      {
        "name": "report",
        "text": "Leaderboard",
        "type": "button",
        "value": "rep",
        "style": "primary"
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
