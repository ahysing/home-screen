import xml, xml.sax
import logging
from .public_transport import Departure

logger = logging.getLogger(__name__)


class DepartureHandler(xml.sax.handler.ContentHandler):
    def __init__(self):
        self.in_monitored_stop_visit = False
        self.in_monitored_vechicle_journey = False
        self.in_expected_departure_time = False
        self.in_destination_display = False
        self.in_delay = False
        self.expected_departure_time = None
        self.destination_name = None
        self.destination_platform_name = None
        self.destination_display = None
        self.line_ref = None
        self.vehicle_mode = None
        self.delay = None
        self.departure_list = []


    def characters(self, content):
        if self.in_destination_name:
            self.destination_name = content
        elif self.in_expected_departure_time:
            self.expected_departure_time = content
        elif self.in_destination_platform_name:
            self.destination_platform_name = content
        elif self.in_destination_display:
            self.destination_display = content
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
            self.in_monitored_vechicle_journey = True
        else:
            if self.in_monitored_stop_visit and self.in_monitored_vechicle_journey:
                if name == 'Delay':
                    self.in_delay = attrs.get('i:nil', 'false') == 'true'
                elif name == 'DestinationName':
                    self.in_destination_name = True
                elif name == 'ExpectedDepartureTime':
                    self.in_expected_departure_time = True
                elif name == 'LineRef':
                    self.in_line_ref = True
                elif name == 'VehicleMode':
                    self.in_vehicle_mode = True


    def endElement(self, name):
        if name == 'MonitoredStopVisit':
            self.in_monitored_stop_visit = False
            d = Departure()
            d.delay = self.delay
            d.destination_name = self.destination_name
            d.expected_departure_time = self.expected_departure_time
            d.destination_display = self.destination_display
            d.destination_platform_name = self.destination_platform_name
            d.line_ref = self.line_ref
            d.vehicle_mode = self.vehicle_mode

            self.departure_list.append(d)
        else:
            self.in_monitored_stop_visit = False
            self.in_monitored_vechicle_journey = False
            self.in_expected_departure_time = False
            self.in_destination_display = False
            self.in_line_ref = False
            self.in_vehicle_mode = False


