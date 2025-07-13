import datetime
import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

import logging
logging.basicConfig(level=logging.DEBUG)
class CalendarService:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/calendar']
        self.creds = None
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', self.SCOPES)
            self.creds = flow.run_local_server(port= 8080)
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())
        self.service = build('calendar', 'v3', credentials=self.creds)

    def create_event(self, data):
        if not data.get("date") or not data.get("time"):
            raise ValueError("Date and time are required to create an event. NLP did not extract them.")

        start = datetime.datetime.strptime(data["date"] + " " + data["time"], "%Y-%m-%d %H:%M")
        end = start + datetime.timedelta(hours=1)
        event = {
            'summary': data["summary"],
            'start': {'dateTime': start.isoformat(), 'timeZone': 'UTC'},
            'end': {'dateTime': end.isoformat(), 'timeZone': 'UTC'},
        }
        created_event = self.service.events().insert(calendarId='primary', body=event).execute()
        return created_event

    def list_events(self):
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        events_result = self.service.events().list(calendarId='primary', timeMin=now,
                                                   maxResults=10, singleEvents=True,
                                                   orderBy='startTime').execute()
        events = events_result.get('items', [])
        return [{"summary": e["summary"], "start": e["start"]} for e in events]

    def delete_event(self, data):
        events = self.service.events().list(calendarId='primary').execute()
        for event in events.get('items', []):
            if data["summary"].lower() in event['summary'].lower():
                self.service.events().delete(calendarId='primary', eventId=event['id']).execute()
                return f"Deleted event: {event['summary']}"
        return "Event not found."
