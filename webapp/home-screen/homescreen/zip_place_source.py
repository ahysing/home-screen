import urllib2
import json
import csv
import logging
import math
from homescreen.zip_place import ZipPlace

logger = logging.getLogger(__name__)


class GeonorgeException(Exception):
    pass


def _parse_postnummer(raw):
    zip_dict = {}
    reader = csv.reader(raw)
    for row in reader:
        zip, place, county, municipality_code, municipality, category_code, category, latitude, longitude = row
        try:
            zip_i = int(zip)
            latitude_n = float(latitude)
            longitude_n = float(longitude)
            zp = ZipPlace(zip_i, latitude_n, longitude_n)
            zip_dict.append(zp)
        except Exception as e:
            logger.error(str(e))
            import pdb
            pdb.set_trace()
    return zip_dict


def fetch_postnummer():
    source_url = 'http://www.bedreinnsikt.no/datasett/DimPostnummer.csv'
    logger.debug(source_url)
    request = urllib2.Request(source_url)
    try:
        response = urllib2.urlopen(request)
        response_body = response.read()
        status_code = response.getcode()
        if status_code == 200:
            return _parse_postnummer(response_body)
        else:
            logger.error("Returned")
            return None
    except urllib2.HTTPError as e:
        return None, e.code
    except urllib2.URLError as e:
        return None, e.code


def _parse_postnummer_closest_to(raw, latitude, longitude):
    json_decoder = json.JSONDecoder()
    try:
        result = json_decoder.decode(raw)
        addresser = result['adresser']
        # web service returns different results types for 1 result than 1 > result
        if not type(addresser) == list:
            addresser = [addresser]
        current_distance = 999
        current_postnummer = None
        for a in addresser:
            try:
                postnummer = a['postnr']
                cur_latitude = a['nord']
                cur_longitude = a['aust']
                cur_latitude_n = float(cur_latitude)
                cur_longitude_n = float(cur_longitude)
                d_x = latitude - cur_latitude_n
                d_y = longitude - cur_longitude_n
                d = math.hypot(d_x, d_y)
                if d < current_distance:
                    current_distance = d
                    current_postnummer = postnummer
            except Exception, e:
                logger.debug(str(e))
        return current_postnummer
    except Exception, e:
        logger.error(str(e))


def fetch_postnummer_closest_to(latitude, longitude, radius=0.1, num_results=1, page=0):
    """
    http://ws.geonorge.no/adresse/dok/AdresseWS_sok.html
    """
    url_template = 'http://ws.geonorge.no/AdresseWS/adresse/radius?nord={latitude}&aust={longitude}&radius={radius}&antPerSide={num_results}&side={page}'

    source_url = url_template.format(latitude=latitude, longitude=longitude, radius=radius, num_results=num_results,
                                     page=page)
    logger.debug(source_url)
    request = urllib2.Request(source_url)
    try:
        response = urllib2.urlopen(request)
        response_body = response.read()
        status_code = response.getcode()
        return response_body, status_code
    except urllib2.HTTPError, e:
        return None, e.code
    except urllib2.URLError, e:
        return None, e.code


def lookup_postnummer_closest_to(latitude, longitude, radius=0.1, num_results=2, page=0):
    latitude = float(latitude)
    longitude = float(longitude)

    response_body, status_code = fetch_postnummer_closest_to(latitude, longitude, radius=radius,
                                                             num_results=num_results, page=page)
    if status_code == 200:
        return _parse_postnummer_closest_to(response_body, latitude, longitude)
    else:
        logger.error("Returned " + str(status_code))
        return None
