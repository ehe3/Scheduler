import json
import webbrowser
import httplib2

from apiclient import discovery
from oauth2client import client


if __name__ == '__main__':
  flow = client.flow_from_clientsecrets(
    'client_secrets.json',
    scope='https://www.googleapis.com/auth/calendar.readonly',
    redirect_uri='urn:ietf:wg:oauth:2.0:oob')

  auth_uri = flow.step1_get_authorize_url()
  webbrowser.open(auth_uri)

  auth_code = raw_input('Enter the auth code: ')

  credentials = flow.step2_exchange(auth_code)
  http_auth = credentials.authorize(httplib2.Http())

  cal_service = discovery.build('calendar', 'v3', http_auth)
  
  page_token = None
  while True:
    calendar_list = cal_service.calendarList().list(pageToken=page_token).execute()
    for calendar_list_entry in calendar_list['items']:
      print calendar_list_entry['summary']
    page_token = calendar_list.get('nextPageToken')
    print page_token
    if not page_token:
      break