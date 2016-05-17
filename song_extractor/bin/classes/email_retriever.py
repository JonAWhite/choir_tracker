# -*- coding: utf-8 -*-
from __future__ import print_function
import sys

if sys.version_info[0] < 3:
    import codecs
    _open_func_bak = open # Make a back up, just in case
    open = codecs.open

import httplib2
import json
import oauth2client
import os

from apiclient import discovery
from oauth2client import client
# from pprint import pprint

from classes.basic_message import BasicMessage, BasicMessages

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

    def __init__(self, client_secret_file, sender_configuration, flags):
        self.client_secret_file = client_secret_file
        self.sender_configuration = sender_configuration
        self.flags = flags
        credentials = self._get_credentials(client_secret_file)
        http = credentials.authorize(httplib2.Http())
        self.service = discovery.build('gmail', 'v1', http=http)
        self._initialize_senders()

    def get_basic_messages(self, sender, search_term, page_token=None, max_results=None):
        """Gets basic messages from GMail

        Args:
            sender (string): Name of person sending the emails
            search_term (string): Term(s) to look for (follows https://support.google.com/mail/answer/7190?hl=en)
            page_token (string): Page token to retrieve a specific page of results in the list.
            max_results (int): Maximum number of messages to return.

        """
        query = "'" + search_term + "' from: " + sender
        print("Query: " + query)
        search_results = self.service.users().messages().list(
            userId='me',
            labelIds=None,
            q=query,
            pageToken=page_token,
            maxResults=max_results).execute()
        message_ids = search_results.get('messages', [])

        # TODO(JWHITE) - add in the page token
        basic_messages = BasicMessages()
        for message_id in message_ids:
            message = self._get_message_from_message_id(message_id)
            basic_messages.append(BasicMessage(message))
        
        return basic_messages

    def _get_message_from_message_id(self, message_id):
        message = self.service.users().messages().get(
                    userId='me', id=message_id['id'],
                    format='full').execute()
        return message

    def _get_credentials(self, client_secret_file):
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
            flow = client.flow_from_clientsecrets(self.client_secret_file, SCOPES)
            flow.user_agent = APPLICATION_NAME
            credentials = tools.run_flow(flow, store, self.flags)
            print('Storing credentials to ' + credential_path)
        return credentials

    def _initialize_senders(self):
        sender_file = open(self.sender_configuration, 'r')
        self.senders = json.load(sender_file)
        # pprint(self.senders)
