import os
from datetime import datetime, timedelta, date
from pathlib import Path
from typing import Tuple, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

ROOT = Path(__file__).resolve().parents[1]
TOKEN_FILE = ROOT / "config/token.json"
CREDENTIALS_FILE = ROOT / "config/credentials.json"
SCOPES = ["https://www.googleapis.com/auth/calendar"]

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

    def create_event(self, title: str, description: str, event_date: Optional[str] = None) -> Tuple[bool, str, str]:
        """
        Creates an all-day calendar event.
        - If event_date is provided (YYYY-MM-DD), it creates it for one day BEFORE that date.
        - If no date is provided, it defaults to tomorrow.
        """
        if not self.service:
            return False, "", "Service not authenticated"

        try:
            if event_date:
                # Convert the email date string to a date object
                base_dt = date.fromisoformat(event_date)
                # Calculate one day before the detected date
                target_date = (base_dt - timedelta(days=1)).isoformat()
            else:
                # Fallback to tomorrow if no date was parsed from email
                target_date = (date.today() + timedelta(days=1)).isoformat()

            event = {
                "summary": title,
                "description": f"Source Email Subject: {description}",
                "start": {"date": target_date},
                "end": {"date": target_date},
                "reminders": {"useDefault": True},
            }

            created_event = self.service.events().insert(calendarId="primary", body=event).execute()
            return True, created_event.get("id", ""), created_event.get("htmlLink", "")
            
        except ValueError:
            return False, "", "Invalid date format provided. Expected YYYY-MM-DD."
        except Exception as e:
            return False, "", f"Failed to create event: {str(e)}"
