import urllib2
import json
import datetime
import logging
import utm
from homescreen import public_transport

logger = logging.getLogger(__name__)


def parse_stopid_for_location(raw):
    json_decoder = json.JSONDecoder()
    stopids = []
    try:
        stops = json_decoder.decode(raw)
        for s in stops:
            stopid = s['ID']
            stopids.append(stopid)
    except Exception as e:
        logger.error(str(e))
    return stopids


def fetch_stopid_for_location(easting, northing, distance=1400):
    """
    http://reisapi.ruter.no/Help/Api/GET-Place-GetClosestStops_proposals_maxdistance
    :param latitude:
    :param longitude:
    :return:
    """
    # TODO: coordinates paramter
    url_template = 'http://reisapi.ruter.no/Place/GetClosestStops?coordinates=(x={northing},y={easting})&proposals={proposals}&maxdistance={distance}'
    proposals = 3
    source_url = url_template.format(proposals=proposals, distance=distance, northing=northing, easting=easting)
    logger.debug(source_url)
    request = urllib2.Request(source_url, headers={'Accepts': 'application/json'})
    try:
        response = urllib2.urlopen(request)
        response_body = response.read()
        status_code = response.getcode()
        return response_body, status_code
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
    distance = 5600
    max_attempts = 6
    stop_ids = []
    logger.debug("Converting WGS84 to UTM33 latitude={0} longitude={1}".format(latitude, longitude))
    latitude_n = 0
    longitude_n = 0
    try:
        latitude_n = float(latitude)
    except ValueError as a:
        logger.error(str(a))
    try:
        longitude_n = float(longitude)
    except ValueError as a:
        logger.error(str(a))
    (easting, northing, zone_number, zone_letter) = utm.from_latlon(latitude_n, longitude_n)
    while len(stop_ids) != 1 and attempts < max_attempts:
        logger.debug('scan_closest_stopid_for_location distance={0} attempt={1}'.format(distance, attempts))
        response_body, status_code = fetch_stopid_for_location(easting, northing, distance=distance)
        if status_code == 200:
            stop_ids = parse_stopid_for_location(response_body)
        else:
            break

        attempts += 1
        distance /= 2

    if len(stop_ids) > 0:
        return \
            stop_ids[0]
    else:
        return None


def parse_transport_for_stop(raw):
    json_decoder = json.JSONDecoder()
    departures = []
    try:
        transports = json_decoder.decode(raw)
        for transport in transports:
            departure = transport['MonitoredVehicleJourney']
            d = public_transport.Departure()
            d.line = departure['LineRef']
            d.line_name = departure['PublishedLineName']
            d.direction = departure['DirectionRef']
            d.direction_name = departure['DirectionName']
            d.destination = departure['DestinationRef']
            d.destination_name = departure['DestinationName']
            d.original_aimed_departure_time = departure['OriginAimedDepartureTime']
            d.destination_aimed_arival_time = departure['DestinationAimedArrivalTime']
            d.delay = departure['Delay']
            departures.append(d)
    except Exception as e:
        logger.error(str(e))
    return public_transport.DepartureResponse(d)


def fetch_transport_for_stop(stop_id, datetime):
    url_template = 'http://reisapi.ruter.no/StopVisit/GetDepartures/{id}?datetime={datetime}'
    #transporttypes = ''  AirportBus,Bus,AirportTrain,Train,Boat,Metro,Tram,""
    # linenames = '' T6,1,2,5,""
    logger.debug('fetch_transport_for_stop stopid={0} datetime={1}'.format(stop_id, datetime))
    source_url = url_template.format(id=stop_id, datetime=datetime)
    logger.debug(source_url)
    request = urllib2.Request(source_url, headers={'Accepts': 'application/json'})
    try:
        response = urllib2.urlopen(request)
        response_body = response.read()
        status_code = response.getcode()
        return response_body, status_code
    except urllib2.HTTPError as e:
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
    stop_id = scan_closest_stopid_for_location(latitude, longitude)
    if stop_id:
        now_text = datetime.datetime.now().isoformat()
        return fetch_transport_for_stop(stop_id, now_text)
    else:
        return None
