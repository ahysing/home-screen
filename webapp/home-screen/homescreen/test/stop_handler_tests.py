# -*- coding: utf-8 -*-
import unittest
from pyramid import testing
from ..stop_handler import StopHandler
from ..public_transport import Stop
import xml.sax
import cStringIO


def parse(raw):
    xml_reader = xml.sax.make_parser()
    stop_handler = StopHandler()
    xml_reader.setContentHandler(stop_handler)
    stream = cStringIO.StringIO(raw)
    xml_reader.parse(stream)
    xml_reader.close()
    return stop_handler.stops


class DepartureHandlerTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parse_emptytag(self):
        pass
