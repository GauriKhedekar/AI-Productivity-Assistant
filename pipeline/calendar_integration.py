import os
import pickle
from datetime import datetime, timedelta
from pathlib import Path
from typing import Tuple

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

ROOT = Path(__file__).resolve().parents[1]
TOKEN_FILE = ROOT / "config/token.json"
CREDENTIALS_FILE = ROOT / "config/credentials.json"
SCOPES = ["https://www.googleapis.com/auth/calendar"]  # Full access to Calendar

class GoogleCalendarIntegration:
    def __init__(self):
        self.service = None

    def authenticate(self) -> Tuple[bool, str]:
        creds = None
        if TOKEN_FILE.exists():
            creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not CREDENTIALS_FILE.exists():
                    return False, "credentials.json missing"
                flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
                creds = flow.run_local_server(port=0)
            with open(TOKEN_FILE, "w") as token:
                token.write(creds.to_json())

        try:
            self.service = build("calendar", "v3", credentials=creds)
            return True, "Authenticated successfully"
        except Exception as e:
            return False, f"Error building service: {str(e)}"

    def create_event(self, title: str, description: str) -> Tuple[bool, str, str]:
        """
        Creates an all-day calendar event for tomorrow.
        Returns (success, event_id, html_link or error message)
        """
        if not self.service:
            return False, "", "Service not authenticated"

        tomorrow = (datetime.utcnow() + timedelta(days=1)).date().isoformat()
        event = {
        "summary": title,
        "description": description,
        "start": {"date": tomorrow},
        "end": {"date": tomorrow},
        "reminders": {"useDefault": True},
         }

        try:
             created_event = self.service.events().insert(calendarId="primary", body=event).execute()
             event_id = created_event.get("id", "")
             # Use the actual htmlLink from the API
             event_link = created_event.get("htmlLink", "")
             return True, event_id, event_link
        except Exception as e:
              return False, "", f"Failed to create event: {str(e)}"
