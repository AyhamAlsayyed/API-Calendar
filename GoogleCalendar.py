# GoogleCalendar.py
import os
import pickle
from datetime import datetime

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class GoogleCalendar:
    SCOPES = ["https://www.googleapis.com/auth/calendar"]

    def __init__(self, credentials_path="credentials.json", token_path="token.pickle"):
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.creds = None
        self.service = None
        self.authenticate()

    def authenticate(self):
        """Authenticate the user and create the service object."""
        if os.path.exists(self.token_path):
            with open(self.token_path, "rb") as token_file:
                self.creds = pickle.load(token_file)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, self.SCOPES
                )
                self.creds = flow.run_local_server(port=0)

            # Save the credentials for next time
            with open(self.token_path, "wb") as token_file:
                pickle.dump(self.creds, token_file)

        self.service = build("calendar", "v3", credentials=self.creds)

    def add_event(self, summary, start_time, end_time, calendar_id="primary"):
        """
        Add a new event to the calendar.
        - summary: str, title of the event
        - start_time, end_time: datetime objects (aware or in UTC)
        Returns the created event as a dictionary.
        """
        event_body = {
            "summary": summary,
            "start": {"dateTime": start_time.isoformat(), "timeZone": "UTC"},
            "end": {"dateTime": end_time.isoformat(), "timeZone": "UTC"},
        }
        event = (
            self.service.events()
            .insert(calendarId=calendar_id, body=event_body)
            .execute()
        )
        return event

    def delete_event(self, event_id, calendar_id="primary"):
        """Delete an event by its ID."""
        self.service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
        return True

    def list_events(self, calendar_id="primary", max_results=10):
        """Return a list of upcoming events."""
        now = datetime.utcnow().isoformat() + "Z"  # 'Z' means UTC
        events_result = (
            self.service.events()
            .list(
                calendarId=calendar_id,
                timeMin=now,
                maxResults=max_results,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        return events_result.get("items", [])
