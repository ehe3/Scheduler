import json
import webbrowser
import httplib2
import datetime
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

  # gets all of the calendar names including multiple pages
  calendars = []
  page_token = None
  while True:
    calendar_list = cal_service.calendarList().list(pageToken=page_token).execute()
    for calendar_list_entry in calendar_list['items']:
      calendars.append(calendar_list_entry['id'])
    page_token = calendar_list.get('nextPageToken')
    if not page_token:
      break

  # loops through each individual calendar to find matches
  curr_date = datetime.datetime.now().date()
  test = datetime.date(2017,2,10)
  page_token = None
  for calendar in calendars:
    while True:
      events = cal_service.events().list(calendarId=calendar, pageToken=page_token).execute()
      for event in events['items']:
        if event['start'].get('dateTime'):
          date_only = event['start']['dateTime'].split('T')
          date_obj = datetime.datetime.strptime(date_only[0], '%Y-%m-%d').date()
        elif event['start'].get('date'):
          date_obj = datetime.datetime.strptime(event['start']['date'], '%Y-%m-%d').date()
        if (date_obj == test):
          print event['summary']
      page_token = events.get('nextPageToken')
      if not page_token:
        break

