# -*- coding: utf-8 -*-
import unittest
import math
from homescreen.zip_place import ZipPlace
from homescreen.zip_place_source import _parse_postnummer_closest_to, _calculate_distance, _sort_zip_place
from pyramid import testing


class ZipPlaceSourceTests(unittest.TestCase):
    def setUp(self):
        self.latitude = 59.90
        self.longitude = 11.23

    def tearDown(self):
        pass

    def test_parse_postnummer_closest_to(self):
        result = _parse_postnummer_closest_to(GEONORGE_RESPONSE, self.latitude, self.longitude)
        self.assertIsInstance(result, list)
        zip = result[0].zip
        self.assertEqual(len(zip), 4)

    def test_parse_postnummer_closest_to_resultTypeIsExpected(self):
        result = _parse_postnummer_closest_to(GEONORGE_RESPONSE, self.latitude, self.longitude)
        self.assertIsInstance(result, list)

    def test_parse_postnummer_closest_to_resultIsNone(self):
        response_empty = '{"sokStatus":{"ok":"true","melding":""},"totaltAntallTreff":"6","adresser":[]}'
        result = _parse_postnummer_closest_to(response_empty, self.latitude, self.longitude)
        self.assertEqual(len(result), 0)

    def test_parse_postnummer_closest_to_resultIsShort(self):
        result = _parse_postnummer_closest_to(GEONORGE_RESPONSE_SHORT_POSTNUMMER, self.latitude, self.longitude)
        self.assertIsInstance(result, list)
        zip = result[0].zip
        self.assertEqual('0476', zip)

    def test__calculate_distance(self):
        latitude = 0
        longitude = 0
        zp = ZipPlace("", latitude=1, longitude=1)
        d = _calculate_distance(zp, latitude, longitude)
        self.assertEqual(d, math.sqrt(2))

    def test__sort_zip_place_none(self):
        latitude = 0
        longitude = 0
        zip_places = [None, None]
        result = _sort_zip_place(zip_places, latitude, longitude)
        self.assertEqual([], result)

    def test__sort_zip_place_none(self):
        latitude = 0
        longitude = 0
        a = ZipPlace('', latitude=1.0, longitude=1.0)
        b = ZipPlace('', latitude=99.0, longitude=99.0)
        zip_places = [a, b]
        result = _sort_zip_place(zip_places, latitude, longitude)
        self.assertEqual([a, b], result)

        zip_places2 = [b, a]
        result2 = _sort_zip_place(zip_places2, latitude, longitude)
        self.assertEqual([a, b], result2)


GEONORGE_RESPONSE = """\
{"sokStatus":{"ok":"true","melding":""},"totaltAntallTreff":"6","adresser":[{"type":"Vegadresse","adressekode":"1740","adressenavn":"Brønnhøydveien","kortadressenavn":"Brønnhøydveien","husnr":"3","undernr":"0","postnr":"1768","poststed":"HALDEN","kommunenr":"0101","kommunenavn":"HALDEN","gardsnr":"159","bruksnr":"49","festenr":"0","seksjonsnr":"0","bruksnavn":"HØYLI","nord":"59.11130121628967","aust":"11.390238202662154"},{"type":"Vegadresse","adressekode":"2165","adressenavn":"Eskevikveien","kortadressenavn":"Eskevikveien","husnr":"10","undernr":"0","postnr":"1768","poststed":"HALDEN","kommunenr":"0101","kommunenavn":"HALDEN","gardsnr":"158","bruksnr":"5","festenr":"0","seksjonsnr":"0","bruksnavn":"HASSELBAKKEN","nord":"59.110749676392295","aust":"11.38750082246196"},{"type":"Vegadresse","adressekode":"1740","adressenavn":"Brønnhøydveien","kortadressenavn":"Brønnhøydveien","husnr":"9","undernr":"0","postnr":"1768","poststed":"HALDEN","kommunenr":"0101","kommunenavn":"HALDEN","gardsnr":"159","bruksnr":"111","festenr":"0","seksjonsnr":"0","bruksnavn":"RØYSA","nord":"59.11115074262135","aust":"11.39060331044053"},{"type":"Vegadresse","adressekode":"2120","adressenavn":"Enerbakken","kortadressenavn":"Enerbakken","husnr":"12","undernr":"0","postnr":"1768","poststed":"HALDEN","kommunenr":"0101","kommunenavn":"HALDEN","gardsnr":"159","bruksnr":"33","festenr":"0","seksjonsnr":"0","bruksnavn":"ATLEHAUG","nord":"59.11179975655192","aust":"11.388730365473847"},{"type":"Vegadresse","adressekode":"1740","adressenavn":"Brønnhøydveien","kortadressenavn":"Brønnhøydveien","husnr":"5","undernr":"0","postnr":"1768","poststed":"HALDEN","kommunenr":"0101","kommunenavn":"HALDEN","gardsnr":"159","bruksnr":"64","festenr":"0","seksjonsnr":"0","bruksnavn":"FURUKOLLEN","nord":"59.11137414839154","aust":"11.389692998054946"},{"type":"Vegadresse","adressekode":"1740","adressenavn":"Brønnhøydveien","kortadressenavn":"Brønnhøydveien","husnr":"7","undernr":"0","postnr":"1768","poststed":"HALDEN","kommunenr":"0101","kommunenavn":"HALDEN","gardsnr":"159","bruksnr":"112","festenr":"0","seksjonsnr":"0","bruksnavn":"RØYSA II","nord":"59.11091651624054","aust":"11.390150265609954"}]}
"""

GEONORGE_RESPONSE_SHORT_POSTNUMMER = """\
{"sokStatus":{"ok":"true","melding":""},"totaltAntallTreff":"1",
"adresser": [{
"type": "Vegadresse",
"adressekode": "10485",
"adressenavn": "Bentsebrugata",
"kortadressenavn": "Bentsebrugata",
"husnr": "20",
"undernr": "0",
"postnr": "476",
"poststed": "OSLO",
"kommunenr": "0301",
"kommunenavn": "OSLO",
"gardsnr": "225",
"bruksnr": "31",
"festenr": "0",
"seksjonsnr": "0",
"bruksnavn": " ",
"nord": "59.93569456941306",
"aust": "10.758670697014356"
}]
}
"""