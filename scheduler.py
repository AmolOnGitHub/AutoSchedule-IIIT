import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def main():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        # Read from JSON and add every necessary event
        event = {
            'organizer': {
                'name': 'AutoScheduler',
            },
            'summary': 'Class_Name',
            'location': 'H105',
            'start': {
                'dateTime': '2024-01-28T09:00:00+05:30',
                'timeZone': 'Asia/Kolkata',
            },
            'end': {
                'dateTime': '2024-01-28T10:00:00+05:30',
                'timeZone': 'Asia/Kolkata',
            },
            'recurrence': [
                'RRULE:FREQ=WEEKLY;UNTIL=20240424T000000Z;BYDAY=TU,TH'
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                {'method': 'popup', 'minutes': 60},
                ],
            },
        }

        event = service.events().insert(calendarId='primary', body=event).execute()
        print ('Event created: %s' % (event.get('htmlLink')))

    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
  main()
