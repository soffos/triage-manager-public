import json
import google.oauth2.credentials
import google_auth_oauthlib.flow

# If modifying these scopes, delete the file src/conf/token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def main():
  """
    Use this script to generate the appropriate authorizations for Google API.
    Requires credentials.json file from Google API hub to be stored at src/conf/gcal_credentials.json
  """
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  cpath = 'src/conf/gcal_token.json'
  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('src/conf/gcal_credentials.json', scopes=SCOPES)

  flow.redirect_uri = 'https://localhost'

  authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')

  print(authorization_url)
  resp = input('url')
  flow.fetch_token(authorization_response=resp)
  credentials = flow.credentials
  print(credentials_to_dict(credentials))
  with open('src/conf/gcal_token.json', 'w') as tok:
    json.dump(credentials_to_dict(credentials), tok)

def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}

if __name__ == '__main__':
  main()
