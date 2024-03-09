import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from loguru import logger


class GmailApi:
    SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

    def __init__(self, config_home: str, credentials_path: str):
        self.config_home = config_home
        self.token_path = os.path.join(config_home, "token.json")
        self.credentials_path = credentials_path
        self._gmail = None
        self._creds = None

    def __enter__(self):
        self.authenticate()
        return self

    def authenticate(self):
        if os.path.exists(self.token_path):
            self._creds = Credentials.from_authorized_user_file(
                self.token_path, self.SCOPES
            )
            if self._creds.valid:
                return
            self._creds.refresh(Request())
            return
        flow = InstalledAppFlow.from_client_secrets_file(
            self.credentials_path, self.SCOPES
        )
        self._creds = flow.run_local_server()
        with open(self.token_path, "w") as token:
            token.write(self._creds.to_json())

    @property
    def gmail(self):
        if not self._gmail:
            self._gmail = build("gmail", "v1", credentials=self._creds)
        return self._gmail

    @property
    def labels(self):
        result = self.gmail.users().labels().list(userId="me").execute()
        labels = result.get("labels", [])
        logger.debug(f"labels: {labels}")
        return labels

    @property
    def status(self):
        if not self._creds:
            return False
        if not self._creds.valid:
            return False
        return True
