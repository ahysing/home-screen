import urllib2
import json
import csv
import logging
import math
import operator
from homescreen.zip_place import ZipPlace

logger = logging.getLogger(__name__)


class GeonorgeException(Exception):
    pass


def _parse_postnummer(raw):
    zip_dict = []
    reader = csv.reader(raw)
    for row in reader:
        zip, place, county, municipality_code, municipality, category_code, category, latitude, longitude = row
        try:
            latitude_n = float(latitude)
            longitude_n = float(longitude)
            zp = ZipPlace(zip, latitude_n, longitude_n, place)
            zip_dict.append(zp)
        except Exception as e:
            logger.error(str(e))
    return _sort_zip_place(zip_dict)


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


def _calculate_distance(zip_place, latitude, longitude):
    d_x = latitude - zip_place.latitude
    d_y = longitude - zip_place.longitude
    return math.hypot(d_x, d_y)


def _sort_zip_place(zip_places, latitude, longitude):
    zip_places = filter(None, zip_places)
    postnummer_distances = [(zp, _calculate_distance(zp, latitude, longitude)) for zp in zip_places]
    postnummer_distances.sort(key=lambda x: operator.itemgetter(1))
    nearest_zip_places = []
    all_postnummer = []
    for pd in postnummer_distances:
        zip = pd[0].zip
        if zip not in all_postnummer:
            all_postnummer.append(zip)
            nearest_zip_places.append(pd[0])
    return nearest_zip_places

def _parse_postnummer_closest_to(raw, latitude, longitude):
    postnummer_word_length = 4
    json_decoder = json.JSONDecoder()
    try:
        result = json_decoder.decode(raw)
        adresser = result['adresser']
        # web service returns different results types for 1 result than 1 > result
        if not type(adresser) == list:
            adresser = [adresser]
        i = 0
        zip_places = [None] * len(adresser)
        for a in adresser:
            try:
                postnummer = a['postnr']
                postnummer_d = postnummer.zfill(postnummer_word_length)
                place = a['poststed']
                cur_latitude = a['nord']
                cur_longitude = a['aust']
                cur_latitude_n = float(cur_latitude)
                cur_longitude_n = float(cur_longitude)
                zip_places[i] = ZipPlace(postnummer_d, cur_latitude_n, cur_longitude_n, place)
                i += 1
            except ValueError as e:
                logger.debug(str(e))
        return _sort_zip_place(zip_places, latitude, longitude)
    except ValueError as e:
        logger.error(str(e))


def fetch_postnummer_closest_to(latitude, longitude, radius=0.1, num_results=25, page=0):
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
    except urllib2.HTTPError as e:
        message = str(e)
        logger.error(message)
        return None, e.getcode()
    except urllib2.URLError as e:
        message = str(e)
        logger.error(message)
        raise GeonorgeException(e)


def lookup_postnummer_closest_to(latitude, longitude, radius=0.1, num_results=25, page=0):
    no_postnummer = []
    latitude = float(latitude)
    longitude = float(longitude)

    response_body, status_code = fetch_postnummer_closest_to(latitude, longitude, radius=radius,
                                                             num_results=num_results, page=page)
    if status_code == 200:
        return _parse_postnummer_closest_to(response_body, latitude, longitude)
    else:
        logger.error("Returned " + str(status_code))
        return no_postnummer
