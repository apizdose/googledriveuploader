from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload,MediaIoBaseDownload


#https://developers.google.com/drive/api/quickstart/python


SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly','https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/drive.appdata','https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/drive.install','https://www.googleapis.com/auth/drive.apps','https://www.googleapis.com/auth/activity','https://www.googleapis.com/auth/drive.metadata','https://www.googleapis.com/auth/drive.scripts']


def main():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:        
        service = build('drive', 'v3', credentials=creds)
        file_metadata = {
        'name': 'testtext.txt'
        }
        media = MediaFileUpload('testtext.txt')
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print ('File ID: ' + file.get('id'))
        
    except HttpError as error:
        print(f'An error occurred: {error}')

if __name__ == '__main__':
    main()