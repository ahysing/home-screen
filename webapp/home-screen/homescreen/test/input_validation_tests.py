# -*- coding: utf-8 -*-
import unittest
from pyramid import testing
from homescreen.input_validation import is_valid_postnummer, is_valid_wgs_84


class InputValidationTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_is_valid_postnummer(self):
        postnummer_large = '10000'
        result_to_large = is_valid_postnummer(postnummer_large)
        self.assertFalse(result_to_large, 'Postnumbers with more than 4 digits are passing')

        postnummer_small = '999'
        result_to_small = is_valid_postnummer(postnummer_small)
        self.assertFalse(result_to_small, 'Postnumber with less than 3 digits are passing')

        postnummer_invalid_number = '-136'
        result_invalid_number = is_valid_postnummer(postnummer_invalid_number)
        self.assertFalse(result_invalid_number, 'Postnumber with negative values are passing')

        postnummer = '1364'
        postnummer_is_valid = is_valid_postnummer(postnummer)
        self.assertTrue(postnummer_is_valid, 'Postnumber 1364 is an actual postnumber and should pass')

        postnumber_zeropadded = '0001'
        postnumber_zeropadded_is_valid = is_valid_postnummer(postnumber_zeropadded)
        self.assertTrue(postnumber_zeropadded_is_valid, 'Postnumber 0001 might be an actual postnumber and should pass')

    def test_is_valid_wgs84_oslo(self):
        # Position source
        # 59° 55' 0" N / 10° 45' 0" E
        # http://www.travelmath.com/cities/Oslo,+Norway
        latitude_oslo = '59.550N'
        longitude_oslo = '10.450E'
        position_oslo_is_valid = is_valid_wgs_84(latitude_oslo, longitude_oslo)
        self.assertTrue(position_oslo_is_valid, 'Latitude and Longitude of Oslo is valid')

    def test_is_valid_wgs_84_bouvet(self):
        # Position source
        # 54°26′48″S 3°21′13″E
        latitude_bouvet = '54.2648S'
        longitude_bouvet = '3.2113E'
        position_bouvet_is_valid = is_valid_wgs_84(latitude_bouvet, longitude_bouvet)
        self.assertTrue(position_bouvet_is_valid, 'Latitude and Longitude of Bouvet is valid')

    def test_is_valid_wgs_84_formBrowser(self):
        # Position source
        # 54°26′48″S 3°21′13″E
        latitude = '59.892136400000005'
        longitude = '10.617284399999999'
        position_is_valid = is_valid_wgs_84(latitude, longitude)
        self.assertTrue(position_is_valid, 'Latitude and Longitude of Bouvet is valid')

# http://localhost:6543/forecast?latitude=59.892136400000005&longitude=10.617284399999999
