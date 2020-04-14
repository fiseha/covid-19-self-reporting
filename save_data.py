from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import configparser

# Read configuration values
config = configparser.ConfigParser()
config.read("config.ini")

SCOPES = [config["GOOGLE"]["SCOPES"]]

# Create a spreadsheet on google sheets and copy the Spreadsheet ID
# ID can be found on the URL of an open sheet
SAMPLE_SPREADSHEET_ID = config["GOOGLE"]["SAMPLE_SPREADSHEET_ID"]
SAMPLE_RANGE_NAME = config["GOOGLE"]["SAMPLE_RANGE_NAME"]


def save_response(values):
    creds = None

    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("sheets", "v4", credentials=creds)

    sheet = service.spreadsheets()

    body = {"values": values}

    return (
        service.spreadsheets()
        .values()
        .append(
            spreadsheetId=SAMPLE_SPREADSHEET_ID,
            range=SAMPLE_RANGE_NAME,
            body=body,
            valueInputOption="USER_ENTERED",
        )
        .execute()
    )
