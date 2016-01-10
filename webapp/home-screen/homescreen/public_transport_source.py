import xml, xml.sax
import urllib2
import json
import datetime
import logging
import utm
from .webutils import get_content_type
from .public_transport import Departure, Stop, DepartureResponse
from .departure_handler import DepartureHandler
from .stop_handler import StopHandler
from .web_service_exception import WebServiceException
import cStringIO
import math
from time_utils import TimeUtils

logger = logging.getLogger(__name__)


class RuterException(WebServiceException):
    pass


def _parse_xml_stops(raw):
    xml_reader = xml.sax.make_parser()
    stream = cStringIO.StringIO(raw)
    stop_handler = StopHandler()
    xml_reader.setContentHandler(stop_handler)
    try:
        xml_reader.parse(stream)
        stream.close()
        return stop_handler.stops
    except xml.sax.SAXParseException as e:
        logger.error(str(e))
        raise RuterException(e)


def _parse_json_stops(raw):
    json_decoder = json.JSONDecoder()
    stops = []
    try:
        response = json_decoder.decode(raw)
        for stop in response:
            s = Stop()
            s.name = stop['Name']
            s.zone = stop['Zone']
            s.is_hub = stop['IsHub'] == 'True'
            s.x = stop['X']
            s.y = stop['Y']
            s.id = stop['ID']
            stops.append(s)
    except KeyError as e:
        logger.error(str(e))
        raise RuterException(e)
    except ValueError as e:
        logger.error(str(e))
        raise RuterException(e)
    return stops


def _parse_json_departures(raw):
    departures = []
    json_decoder = json.JSONDecoder()
    transports = json_decoder.decode(raw)
    for transport in transports:
        try:
            d = Departure()
            monitored_vehicle_journey = transport['MonitoredVehicleJourney']
            d.vehicle_mode = monitored_vehicle_journey['VehicleMode']
            d.line_ref = monitored_vehicle_journey['LineRef']
            d.direction_ref = monitored_vehicle_journey['DirectionRef']
            d.published_line_name = monitored_vehicle_journey['PublishedLineName']
            d.direction_name = monitored_vehicle_journey['DirectionName']
            d.destination_name = monitored_vehicle_journey['DestinationName']
            d.delay = monitored_vehicle_journey['Delay']

            monitor_call = monitored_vehicle_journey['MonitoredCall']
            d.destination_display = monitor_call['DestinationDisplay']
            d.aimed_departure_time = monitor_call['AimedDepartureTime']
            d.expected_departure_time = monitor_call['ExpectedDepartureTime']
            departures.append(d)
        except KeyError as e:
            logger.error(str(e))
            raise RuterException(e)
        except ValueError as e:
            logger.error(str(e))
            raise RuterException(e)
    return departures


def _parse_xml_departures(raw):
    sax_xmlreader = xml.sax.make_parser()
    departure_handler = DepartureHandler()
    stream = cStringIO.StringIO(raw)
    try:
        sax_xmlreader.setContentHandler(departure_handler)
        sax_xmlreader.parse(stream)
        stream.close()
        return departure_handler.departures
    except xml.sax.SAXParseException as e:
        logger.error(str(e))
        raise RuterException(e)

def _parse_stopid_for_location(raw, content_type):
    d = None
    if raw:
        first = raw[0]
        if content_type in ['text/xml', 'text/xml; charset=utf-8', 'application/xml', 'application/xml; charset=utf-8']:
            logger.debug('content type for stopid by location. using XML')
            d = _parse_xml_stops(raw)
        elif content_type in ['application/json', 'application/json; charset=utf-8']:
            logger.debug('content type for stopid by location. using JSON')
            d = _parse_json_stops(raw)
        elif first == '<':
            logger.warning('unknown content type for stopid by location. Assuming XML')
            d = _parse_xml_stops(raw)
        elif first in ['[', '{', '"']:
            logger.warning('unknown content type for stopid by location. Assuming JSON')
            d = _parse_json_stops(raw)
        else:
            logger.error('Content-Type {}'.format(content_type))
            raise RuterException(error="unknown parse format for stopID")
    return d


def fetch_stopid_for_location(easting, northing, distance=1400):
    """
    http://reisapi.ruter.no/Help/Api/GET-Place-GetClosestStops_proposals_maxdistance
    :param latitude:
    :param longitude:
    :return:
    """
    service_reis_timeout = 14 # 7.603 seconds is the highest tieout we have seen from that service so far
    # TODO: coordinates paramter
    url_template = 'http://reisapi.ruter.no/Place/GetClosestStops?coordinates=(x={easting},y={northing})&maxdistance={distance}'
    source_url = url_template.format(distance=int(distance), easting=easting, northing=northing)
    logger.debug(source_url)
    request = urllib2.Request(source_url, headers={'Accepts': 'application/xml'})
    try:
        response = urllib2.urlopen(request, timeout=service_reis_timeout)
        content_type = get_content_type(response)
        response_body = response.read()
        status_code = response.getcode()
        return response_body, status_code, content_type
    except urllib2.HTTPError as e:
        logger.error(str(e))
        return None, e.getcode()
    except urllib2.URLError as e:
        logger.error(str(e))
        raise RuterException(e)


def _get_closest_stop_by_distance(stop_ids, center_x, center_y):
    shortest_stop_distance = float('inf')
    shortest_stop = None

    if len(stop_ids) > 1:
        for stop in stop_ids:
            d_x = center_x - stop.x
            d_y = center_y - stop.y
            stop_distance = math.hypot(d_x, d_y)
            if stop_distance <= shortest_stop_distance:
                shortest_stop_distance = stop_distance
                shortest_stop = stop
                logger.debug('Updating closest stop {}'.format(stop.__json__(None)))
    elif len(stop_ids) == 1:
        shortest_stop = stop_ids[0]
    return shortest_stop


def scan_closest_stopid_for_location(latitude, longitude):
    attempts = 0
    distance = 500
    max_attempts = 6
    stop_ids = []
    logger.debug("Converting WGS84 to UTM33 latitude={0} longitude={1}".format(latitude, longitude))
    latitude_n = 0
    longitude_n = 0
    try:
        latitude_n = float(latitude)
    except ValueError as e:
        logger.error(str(e))

    try:
        longitude_n = float(longitude)
    except ValueError as a:
        logger.error(str(a))
    (easting, northing, zone_number, zone_letter) = utm.from_latlon(latitude_n, longitude_n)
    easting_i = int(easting)
    northing_i = int(northing)
    while len(stop_ids) == 0 and attempts < max_attempts:
        logger.debug('scan_closest_stopid_for_location distance={0} attempt={1}'.format(int(distance), attempts))
        response_body, status_code, content_type = fetch_stopid_for_location(easting_i, northing_i, distance=distance)
        if status_code == 200:
            stop_ids = _parse_stopid_for_location(response_body, content_type)
        attempts += 1
        for i in range(attempts):
            distance *= 2

    shortest_stop = _get_closest_stop_by_distance(stop_ids, easting, northing)
    return shortest_stop


def _parse_transport_for_stop(raw, content_type):
    d = None
    if raw:
        first = raw[0]
        if content_type in ['text/xml', 'text/xml; charset=utf-8', 'application/xml', 'application/xml; charset=utf-8']:
            logger.debug('content type for transport by stop. using XML')
            d = _parse_xml_departures(raw)
        elif content_type in ['application/json', 'application/json; charset=utf-8']:
            logger.debug('content type for transport by stop. using JSON')
            d = _parse_json_departures(raw)
        elif first == '<':
            logger.warning('unknown content type for transport by stop. Assuming XML')
            d = _parse_xml_departures(raw)
        elif first in ['[', '{', '"']:
            logger.warning('unknown content type for transport by stop. Assuming JSON')
            d = _parse_json_departures(raw)
        else:
            logger.error('Content-Type {}'.format(content_type))
            raise RuterException(error="unknown parse format for stopID")
    return d


def fetch_transport_for_stop(stop, datetime):
    url_template = 'http://reisapi.ruter.no/StopVisit/GetDepartures/{id}?datetime={datetime}'
    # transporttypes = ''  AirportBus,Bus,AirportTrain,Train,Boat,Metro,Tram,""
    # linenames = '' T6,1,2,5,""
    stop_id = stop.id
    logger.debug('fetch_transport_for_stop stopid={0} datetime={1}'.format(stop_id, datetime))
    source_url = url_template.format(id=stop_id, datetime=datetime)
    logger.debug(source_url)
    request = urllib2.Request(source_url, headers={'Accepts': 'application/json'})
    try:
        response = urllib2.urlopen(request)
        content_type = get_content_type(response)
        response_body = response.read()
        status_code = response.getcode()
        return response_body, status_code, content_type
    except urllib2.HTTPError as e:
        logger.error(str(e))
        return None, e.getcode()
    except urllib2.URLError as e:
        logger.error(str(e))
        raise RuterException(e)


def lookup_transport_for_stop(latitude, longitude, limit=-1):
    """
    documentation for departures
    http://reisapi.ruter.no/Help/Api/GET-StopVisit-GetDepartures-id_datetime_transporttypes_linenames
    :param latitude:
    :param longitude:
    :return:
    """
    logger.debug('lookup_transport_for_stop latitude={0} longitude={1}'.format(latitude, longitude))
    departure_response = DepartureResponse()
    stop = scan_closest_stopid_for_location(latitude, longitude)
    if stop:
        half_hour_m = 0
        next_half_hour_date = TimeUtils().systemtime() + datetime.timedelta(minutes=half_hour_m)
        next_half_hour = next_half_hour_date.isoformat()
        response_body, status_code, content_type = fetch_transport_for_stop(stop, next_half_hour)
        if status_code == 200:
            departures = _parse_transport_for_stop(response_body, content_type)
            departure_response.stop = stop
            if limit >= 0:
                size = min(len(departures), limit)
                departures = departures[:size]
            departure_response.departures = departures
        else:
            logger.error('fetch_transport_for_stop returned HTTP status {}'.format(status_code))
    else:
        departure_response.departures = []
        logger.warn('No stop found nearby. unable to return results')
    return departure_response
