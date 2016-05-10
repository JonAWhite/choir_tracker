from __future__ import print_function
import base64
import email
import httplib2
import json
import os
import re

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = '../conf/client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def get_full_body( message, mimeType ):
    parts = message['payload']['parts'];
    full_body = ""
    for part in parts:
        if part['mimeType'] != mimeType:
            continue
        else:
            data = part['body']['data']
            full_body = base64.urlsafe_b64decode(data.encode('ascii'))

    return full_body

def get_header_value( message, name ):
    headers = message['payload']['headers'];
    date = ""
    for header in headers:
        if header['name'] != name:
            continue
        else:
            date = header['value'] 

    return date; 

# def get_songs_from_text( text ):
    # lines = text.splitlines()
    # lines_with_numbers = re.findall(r'0-9', lines)


def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    search_results = service.users().messages().list(userId='me', labelIds=None, q='"Songs for Sunday" from: Jason Baisch', maxResults=2).execute()
    messages = search_results.get('messages', [])

    if not messages:
        print('No messages found.')
    else:
      print('Messages:')
      for message in messages:
        email_results = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
        subject = get_header_value(email_results, "Subject")
        date = get_header_value(email_results, "Date")
        body = get_full_body(email_results, "text/plain")

if __name__ == '__main__':
    main()
