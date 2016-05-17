# -*- coding: utf-8 -*-
"""Provides easy access to key features of the underlying message

Example::

    from classes.basic_message import BasicMessage
    basic_message = BasicMessage(message)
    subject = basic_message.get_header_value("Subject")
    text = basic_message.get_full_body("text/plain")
    html = basic_message.get_full_body("text/html")

"""

import base64
import json

class BasicMessage(object):
    """A basic message which allows easier access to the underlying message
    from gmail

    https://developers.google.com/gmail/api/v1/reference/users/messages#resource-representations

    Args:
        message (str): JSON message string from gmail

    """

    def __init__(self, message):
        self.message = message 

    def get_full_body(self, mime_type):
        """Get the full body from the message

        Args:
            mime_type: The mime type to get. Examples are 'text/plain' and
            'text/html'

        Returns:
            Unicode message in the format requested

        """
        parts = []
        if 'parts' in self.message['payload'].keys():
            parts = self.message['payload']['parts']
        else:
            print json.dumps(self.message['payload'])
            parts = [ self.message['payload'] ]

        full_body = ""
        for part in parts:
            if part['mimeType'] != mime_type:
                continue
            else:
                data = part['body']['data']
                full_body = base64.urlsafe_b64decode(data.encode(
                    'utf-8')).decode('utf-8')

        return full_body

    def get_header_value(self, name):
        """Gets the value of the associated header name

        Args:
            name: The name of the header. Examples are Subject and Date

        Returns:
            Unicode value associated with the header name

        """
        headers = self.message['payload']['headers']
        date = ""
        for header in headers:
            if header['name'] != name:
                continue
            else:
                date = header['value']

        return date

class BasicMessages(list):
    def __init__(self, page_token=None):
        list.__init__([])
        self.page_token = page_token

