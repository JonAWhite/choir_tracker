# -*- coding: utf-8 -*-
from __future__ import print_function
import sys

if sys.version_info[0] < 3:
    import codecs
    _open_func_bak = open # Make a back up, just in case
    open = codecs.open

import httplib2
# import json
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
from classes.jason_song_list_extractor import JasonSongListExtractor

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
APPLICATION_NAME = 'Gmail API Python Quickstart'

class EmailRetriever:
    """Uses the GMail API to pull messages with a specific subject from specific_people 

    Args:
        client_secret_file:   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
        sender_configuration: JSON file to specify who to retrieve emails from and what to look for

    Example Sender Configuration:

    .. code-block:: json

        {
         "Sender": [
          {"Name": "Barb Schenk", "Search": "Songs for"},
          {"Name": "Jason Baisch", "Search": "Songs for"},
          {"Name": "Jonathan White", "Search": "Songs for"}
         ]
        }

    Developer Resources:
        https://developers.google.com/gmail/api/auth/web-server#create_a_client_id_and_client_secret
        https://developers.google.com/resources/api-libraries/documentation/gmail/v1/python/latest/gmail_v1.users.messages.html


    """

    def __init__(self, client_secret_file, sender_configuration):
        self.sender_configuration = sender_configuration
        credentials = self._get_credentials(client_secret_file)
        http = credentials.authorize(httplib2.Http())
        self.service = discovery.build('gmail', 'v1', http=http)

    def get_basic_messages(self, sender, search_term, page_token=None, max_results=None):
        """Gets basic messages from GMail

        Args:
            sender (string): Name of person sending the emails
            search_term (string): Term(s) to look for (follows https://support.google.com/mail/answer/7190?hl=en)
            page_token (string): Page token to retrieve a specific page of results in the list.
            max_results (int): Maximum number of messages to return.

        """
        query = '"' + search_term + "' from: " + sender
        search_results = self.service.users().messages().list(
            userId='me',
            labelIds=None,
            q=query,
            pageToken=page_token,
            maxResults=max_results).execute()
        messages = search_results.get('messages', [])

    def _get_credentials(this, client_secret_file):
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
            flow = client.flow_from_clientsecrets(this.client_secret_file, SCOPES)
            flow.user_agent = APPLICATION_NAME
            flags = tools.argparser.parse_args(args=[])
            credentials = tools.run_flow(flow, store, flags)
            print('Storing credentials to ' + credential_path)
        return credentials

