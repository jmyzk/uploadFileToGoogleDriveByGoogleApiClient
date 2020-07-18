"""
usint google api client, upload files from local windows pc.
"""

from __future__ import print_function
import pickle
import fnmatch
import os.path
from googleapiclient.discovery import build
from googleapiclient.discovery import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

def main():
    creds = None
    # this code come from google quick start
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)
    mydir = 'c:/orange/customers.'
    # get the list of files with a pattern cliteria and upload each of them
    listOfFiles = os.listdir(mydir)
    pattern = "*.csv"
    for entry in listOfFiles:
        if fnmatch.fnmatch(entry, pattern):
            file_metadata = {'name': entry}
            path = os.path.join(mydir, entry)
            # this is the second way to upload files less than 5G shown in the quickstart.
            # use mintype='text/csv' for csv
            media = MediaFileUpload(path, mimetype='text/csv')
            file = service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()
            print ('File ID: %s' % file.get('id'))

if __name__ == '__main__':
    main()
