import xml, xml.sax
import urllib2
import json
import datetime
import logging
import utm
from .public_transport import Departure, Stop
from .departure_handler import DepartureHandler
from .stop_handler import StopHandler
import cStringIO

logger = logging.getLogger(__name__)


class RuterException(Exception):
    pass


def parse_xml_stops(raw):
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


def parse_json_stops(raw):
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


def parse_json_departures(raw):
    json_decoder = json.JSONDecoder()
    departures = []
    try:
        transports = json_decoder.decode(raw)
        for transport in transports:
            d = Departure()

            monitored_vehicle_journey = transport['MonitoredVehicleJourney']
            d.line_ref = monitored_vehicle_journey['LineRef']
            d.direction_ref = monitored_vehicle_journey['DirectionRef']
            d.published_line_name = monitored_vehicle_journey['PublishedLineName']
            d.direction_name = monitored_vehicle_journey['DirectionName']
            d.destination_name = monitored_vehicle_journey['DestinationName']
            d.original_aimed_departure_time = monitored_vehicle_journey['OriginAimedDepartureTime']
            d.destination_aimed_arrival_time = monitored_vehicle_journey['DestinationAimedArrivalTime']
            d.delay = monitored_vehicle_journey['Delay']

            monitor_call = monitored_vehicle_journey['MonitoredCall']
            d.destination_aimed_arrival_time = monitor_call['AimedArrivalTime']

            departures.append(d)
    except KeyError as e:
        logger.error(str(e))
        raise RuterException(e)
    except ValueError as e:
        logger.error(str(e))
        raise RuterException(e)
    return departures


def parse_xml_departures(raw):
    sax_xmlreader = xml.sax.make_parser()
    departure_handler = DepartureHandler()
    stream = cStringIO.StringIO(raw)
    try:
        sax_xmlreader.setContentHandler(departure_handler)
        sax_xmlreader.parse(stream)
        stream.close()
        return departure_handler.departures
    except xml.sax.SAXParseException as e:
        import pdb
        pdb.set_trace()
        logger.error(str(e))


def parse_stopid_for_location(raw, content_type):
    d = None
    if raw:
        first = raw[0]
        if content_type in ['text/xml', 'application/xml']:
            logger.debug('content type for stopid by location. using XML')
            d = parse_xml_stops(raw)
        elif content_type in ['application/json']:
            logger.debug('content type for stopid by location. using JSON')
            d = parse_json_stops(raw)
        elif first == '<':
            logger.warning('unknown content type for stopid by location. Assuming XML')
            d = parse_xml_stops(raw)
        elif first in ['[', '{', '"']:
            logger.warning('unknown content type for stopid by location. Assuming JSON')
            d = parse_json_stops(raw)
        else:
            raise RuterException("unknown parse format for stopID")
    return d


def fetch_stopid_for_location(easting, northing, distance=1400):
    """
    http://reisapi.ruter.no/Help/Api/GET-Place-GetClosestStops_proposals_maxdistance
    :param latitude:
    :param longitude:
    :return:
    """
    # TODO: coordinates paramter
    url_template = 'http://reisapi.ruter.no/Place/GetClosestStops?coordinates=(x={easting},y={northing})&proposals={proposals}&maxdistance={distance}'
    proposals = 3
    source_url = url_template.format(proposals=proposals, distance=distance, easting=easting, northing=northing)
    logger.debug(source_url)
    request = urllib2.Request(source_url, headers={'Accepts': 'application/xml'})
    try:
        response = urllib2.urlopen(request)
        content_type = response.headers.get('Content-Type')
        response_body = response.read()
        status_code = response.getcode()
        return response_body, status_code, content_type
    except urllib2.HTTPError as e:
        import pdb
        pdb.set_trace()
        logger.error(str(e))
        return None, e.getcode()
    except urllib2.URLError as e:
        import pdb
        pdb.set_trace()
        logger.error(str(e))
        return None, e.code


def scan_closest_stopid_for_location(latitude, longitude):
    attempts = 0
    distance = 87.5
    max_attempts = 4
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
    while len(stop_ids) != 1 and attempts < max_attempts:
        logger.debug('scan_closest_stopid_for_location distance={0} attempt={1}'.format(distance, attempts))
        response_body, status_code, content_type = fetch_stopid_for_location(easting_i, northing_i, distance=distance)
        if status_code == 200:
            stop_ids = parse_stopid_for_location(response_body, content_type)
        attempts += 1
        for i in range(attempts):
            distance *= 2
    return stop_ids


# deprecated: unused
def parse_transport_for_stop(raw, content_type):
    d = None
    if raw:
        first = raw[0]
        if content_type in ['text/xml', 'application/xml']:
            logger.debug('content type for stopid by location. using XML')
            d = parse_xml_departures(raw)
        elif content_type in ['application/json']:
            logger.debug('content type for stopid by location. using JSON')
            d = parse_json_departures(raw)
        elif first == '<':
            logger.warning('unknown content type for stopid by location. Assuming XML')
            d = parse_xml_departures(raw)
        elif first in ['[', '{', '"']:
            logger.warning('unknown content type for stopid by location. Assuming JSON')
            d = parse_json_departures(raw)
        else:
            raise RuterException("unknown parse format for stopID")
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
        content_type = response.headers.get('Content-Type')
        response_body = response.read()
        status_code = response.getcode()
        return response_body, status_code, content_type
    except urllib2.HTTPError as e:
        import pdb
        pdb.set_trace()
        logger.error(str(e))
        return None, e.getcode()
    except urllib2.URLError as e:
        logger.error(str(e))
        return None, e.code


def lookup_transport_for_stop(latitude, longitude):
    """
    documenation for location lookup


    documentation for departures
    http://reisapi.ruter.no/Help/Api/GET-StopVisit-GetDepartures-id_datetime_transporttypes_linenames
    :param latitude:
    :param longitude:
    :return:
    """
    logger.debug('lookup_transport_for_stop latitude={0} longitude={1}'.format(latitude, longitude))
    transports = []
    stops = scan_closest_stopid_for_location(latitude, longitude)
    if stops:
        now_text = datetime.datetime.now().isoformat()
        for s in stops:
            transport_list = fetch_transport_for_stop(s, now_text)
            transports.extend(transport_list)
    return transports
