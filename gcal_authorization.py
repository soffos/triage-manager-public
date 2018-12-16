import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file src/conf/token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar'

def main():
  """
    Use this script to generate the appropriate authorizations for Google API.
    Requires credentials.json file from Google API hub to be stored at src/conf/gcal_credentials.json
  """
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  store = file.Storage('src/conf/gcal_token.json')
  creds = store.get()
  if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('src/conf/gcal_credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)

if __name__ == '__main__':
  main()