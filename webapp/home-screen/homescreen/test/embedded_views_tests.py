# -*- coding: utf-8 -*-
import unittest
from pyramid import testing
from homescreen.embedded_views import _filter_forecast_date, _filter_forecast_fields
import datetime
from homescreen.weather import Time


class EmbeddedViewsTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test__filter_forecast_date(self):
        date = datetime.datetime(2015,1, 1, 0, 0)
        fc = [
            Time(),
            Time()
        ]
        result = _filter_forecast_date(fc, date)
        self.assertTrue(1, len(result))

    def test__filter_forecast_fields(self):
        fc = [
            Time(),
            Time()
        ]
        keys = ['start', 'to']
        result = _filter_forecast_fields(fc, keys)
        seen_keys = map(lambda x: x.keys(), result)
        actual_keys = list(set(seen_keys))
        self.assertTrue(keys, actual_keys)