# -*- coding: utf-8 -*-
import urllib2
import xml, xml.sax
import cStringIO
from .weather import WeatherResponse, Credit, Time, Place
from .weather_handler import WeatherHandler
import logging

logger = logging.getLogger(__name__)


class YrException(Exception):
    pass


def _parse_forecast(raw):
    sax_xml_parser = xml.sax.make_parser()
    stream = cStringIO.StringIO(raw)
    try:
        weather_handler = WeatherHandler()
        sax_xml_parser.setContentHandler(weather_handler)
        sax_xml_parser.parse(stream)
        stream.close()
        wr = WeatherResponse()
        wr.credit = weather_handler.credit
        wr.place = weather_handler.place
        wr.time_forecasts = weather_handler.time_forecasts
        return wr
    except xml.sax.SAXParseException as e:
        logger.error(str(e))
        raise YrException(e)
    return None


def lookup_forecast_for_postnummer(postnummer):
    response_body, status_code = fetch_forecast_for_postnummer(postnummer)
    if status_code == 200:
        return _parse_forecast(response_body)
    else:
        logger.warning('Failed to get forecast for %s. HTTP Response code', postnummer, status_code)
        wr = WeatherResponse()
        wr.credit = Credit()
        wr.place = Place()
        wr.time_forecasts = []
        return wr


def fetch_forecast_for_postnummer(postnummer):
    postnummer_s = postnummer
    source_url_template = 'http://yr.no/sted/Norge/postnummer/{postnummer}/varsel.xml'
    source_url = source_url_template.format(postnummer=postnummer_s)
    logger.debug(source_url)
    request = urllib2.Request(source_url)
    try:
        response = urllib2.urlopen(request)
        response_body = response.read()
        status_code = response.getcode()
        return response_body, status_code
    except urllib2.HTTPError as e:
        message = str(e)
        logger.error(message)
        return None, e.code
    except urllib2.URLError as e:
        message = str(e)
        logger.error(message)
        raise YrException(e)