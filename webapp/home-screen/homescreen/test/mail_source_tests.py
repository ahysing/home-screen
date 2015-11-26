# -*- coding: utf-8 -*-
import unittest
from pyramid import testing
from homescreen.mail_source import MailSource, MsExchangeException

class MailSourceTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_constructor(self):
        ROOT_URL = ''
        mail_source = MailSource(ROOT_URL)
        self.assertTrue(True)

    def test_lookup_calendar_to(self):
        pass