import xml, xml.sax
import logging

from .public_transport import Departure

logger = logging.getLogger(__name__)


class DepartureHandler(xml.sax.handler.ContentHandler):
    def __init__(self):
        self.in_delay = False
        self.in_destination_name = False
        self.in_destination_platform_name = False
        self.in_line_ref = False
        self.in_monitored_stop_visit = False
        self.in_monitored_vehicle_journey = False
        self.in_expected_departure_time = False
        self.in_destination_display = False
        self.in_vehicle_mode = False
        self.in_destination_aimed_arrival_time = False
        self.in_direction_name = False
        self.in_original_aimed_departure_time = False
        self.set_fields_none()
        self.departures = []


    def set_fields_none(self):
        self.original_aimed_departure_time = None
        self.destination_aimed_arrival_time = None
        self.expected_departure_time = None
        self.destination_name = None
        self.destination_platform_name = None
        self.destination_display = None
        self.direction_name = None
        self.line_ref = None
        self.vehicle_mode = None
        self.delay = None


    def characters(self, content):
        if self.in_destination_name:
            self.destination_name = content
        elif self.in_expected_departure_time:
            self.expected_departure_time = content
        elif self.in_destination_platform_name:
            self.destination_platform_name = content
        elif self.in_original_aimed_departure_time:
            self.original_aimed_departure_time = content
        elif self.in_destination_aimed_arrival_time:
            self.destination_aimed_arrival_time = content
        elif self.in_destination_display:
            self.destination_display = content
        elif self.in_direction_name:
            self.direction_name = content
        elif self.in_line_ref:
            self.line_ref = content
        elif self.in_vehicle_mode:
            self.vehicle_mode = content
        elif self.in_delay:
            self.delay = content


    def startElement(self, name, attrs):
        if name == 'MonitoredStopVisit':
            self.in_monitored_stop_visit = True
        elif name == 'MonitoredVehicleJourney':
            self.in_monitored_vehicle_journey = True
        else:
            if self.in_monitored_stop_visit and self.in_monitored_vehicle_journey:
                if name == 'Delay':
                    self.in_delay = True
                elif name == 'DestinationName':
                    self.in_destination_name = True
                elif name == 'OriginAimedDepartureTime':
                    self.in_original_aimed_departure_time = True
                elif name == 'DestinationAimedArrivalTime':
                    self.in_destination_aimed_arrival_time = True
                elif name == 'DirectionName':
                    self.in_direction_name = True
                elif name == 'ExpectedDepartureTime':
                    self.in_expected_departure_time = True
                elif name == 'LineRef':
                    self.in_line_ref = True
                elif name == 'VehicleMode':
                    self.in_vehicle_mode = True



    def push_all_fields(self):
        d = Departure()
        d.delay = self.delay
        d.destination_name = self.destination_name
        d.destination_aimed_arrival_time = self.destination_aimed_arrival_time
        d.expected_departure_time = self.expected_departure_time
        d.destination_display = self.destination_display
        d.destination_platform_name = self.destination_platform_name
        d.direction_name = self.direction_name
        d.line_ref = self.line_ref
        d.vehicle_mode = self.vehicle_mode
        self.departures.append(d)


    def endElement(self, name):
        if name == 'MonitoredStopVisit':
            self.in_monitored_stop_visit = False
            self.push_all_fields()
            self.set_fields_none()
        elif name == 'MonitoredVehicleJourney':
            self.in_monitored_vehicle_journey = False
        elif name == 'Delay':
            self.in_delay = False
        elif name == 'DestinationName':
            self.in_destination_name = False
        elif name == 'DestinationAimedArrivalTime':
            self.in_destination_aimed_arrival_time = False
        elif name == 'DirectionName':
            self.in_direction_name = False
        elif name == 'ExpectedDepartureTime':
            self.in_expected_departure_time = False
        elif name == 'LineRef':
            self.in_line_ref = False
        elif name == 'VehicleMode':
            self.in_vehicle_mode = False
        elif name == 'OriginalAimedArrivalTime':
            self.in_original_aimed_departure_time = False

