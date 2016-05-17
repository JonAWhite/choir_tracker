# -*- coding: utf-8 -*-
import unittest
from classes.email_retriever import EmailRetriever

class EmailRetrieverTestCase(unittest.TestCase):
    
    def test_initialize_senders(self):
        email_retriever = EmailRetriever('../../conf/client_secret.json', '../../conf/sender_configuration.json')
        self.assertEquals(email_retriever.senders["Sender"][0]["Name"], u"Barb Schenk")

