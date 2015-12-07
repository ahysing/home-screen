# -*- coding: utf-8 -*-
import unittest
from homescreen.zip_place_source import _parse_postnummer_closest_to
from pyramid import testing


class ZipPlaceSourceTests(unittest.TestCase):
    def setUp(self):
        self.latitude = 59.90
        self.longitude = 11.23

    def tearDown(self):
        pass

    def test_parsePostnummerClosestTo(self):
        result = _parse_postnummer_closest_to(GEONORGE_RESPONSE, self.latitude, self.longitude)
        self.assertIsInstance(result, unicode)
        self.assertEqual(len(result), 4)

    def test_parsePostnummerClosestTo_resultTypeIsExpected(self):
        result = _parse_postnummer_closest_to(GEONORGE_RESPONSE, self.latitude, self.longitude)
        self.assertIsInstance(result, unicode)

    def test_parsePostnummerClosestTo_resultIsNone(self):
        response_empty = '{"sokStatus":{"ok":"true","melding":""},"totaltAntallTreff":"6","adresser":[]}'
        result = _parse_postnummer_closest_to(response_empty, self.latitude, self.longitude)
        self.assertIsNone(result)

GEONORGE_RESPONSE = """\
{"sokStatus":{"ok":"true","melding":""},"totaltAntallTreff":"6","adresser":[{"type":"Vegadresse","adressekode":"1740","adressenavn":"Brønnhøydveien","kortadressenavn":"Brønnhøydveien","husnr":"3","undernr":"0","postnr":"1768","poststed":"HALDEN","kommunenr":"0101","kommunenavn":"HALDEN","gardsnr":"159","bruksnr":"49","festenr":"0","seksjonsnr":"0","bruksnavn":"HØYLI","nord":"59.11130121628967","aust":"11.390238202662154"},{"type":"Vegadresse","adressekode":"2165","adressenavn":"Eskevikveien","kortadressenavn":"Eskevikveien","husnr":"10","undernr":"0","postnr":"1768","poststed":"HALDEN","kommunenr":"0101","kommunenavn":"HALDEN","gardsnr":"158","bruksnr":"5","festenr":"0","seksjonsnr":"0","bruksnavn":"HASSELBAKKEN","nord":"59.110749676392295","aust":"11.38750082246196"},{"type":"Vegadresse","adressekode":"1740","adressenavn":"Brønnhøydveien","kortadressenavn":"Brønnhøydveien","husnr":"9","undernr":"0","postnr":"1768","poststed":"HALDEN","kommunenr":"0101","kommunenavn":"HALDEN","gardsnr":"159","bruksnr":"111","festenr":"0","seksjonsnr":"0","bruksnavn":"RØYSA","nord":"59.11115074262135","aust":"11.39060331044053"},{"type":"Vegadresse","adressekode":"2120","adressenavn":"Enerbakken","kortadressenavn":"Enerbakken","husnr":"12","undernr":"0","postnr":"1768","poststed":"HALDEN","kommunenr":"0101","kommunenavn":"HALDEN","gardsnr":"159","bruksnr":"33","festenr":"0","seksjonsnr":"0","bruksnavn":"ATLEHAUG","nord":"59.11179975655192","aust":"11.388730365473847"},{"type":"Vegadresse","adressekode":"1740","adressenavn":"Brønnhøydveien","kortadressenavn":"Brønnhøydveien","husnr":"5","undernr":"0","postnr":"1768","poststed":"HALDEN","kommunenr":"0101","kommunenavn":"HALDEN","gardsnr":"159","bruksnr":"64","festenr":"0","seksjonsnr":"0","bruksnavn":"FURUKOLLEN","nord":"59.11137414839154","aust":"11.389692998054946"},{"type":"Vegadresse","adressekode":"1740","adressenavn":"Brønnhøydveien","kortadressenavn":"Brønnhøydveien","husnr":"7","undernr":"0","postnr":"1768","poststed":"HALDEN","kommunenr":"0101","kommunenavn":"HALDEN","gardsnr":"159","bruksnr":"112","festenr":"0","seksjonsnr":"0","bruksnavn":"RØYSA II","nord":"59.11091651624054","aust":"11.390150265609954"}]}
"""