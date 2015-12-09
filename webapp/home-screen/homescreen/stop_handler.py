import xml.sax
from public_transport import Stop
import logging

logger = logging.getLogger(__name__)


class StopHandler(xml.sax.ContentHandler):
    """
    A SAX parser for which converts bus, plane, ferry and rail stops from valid XML documents into a list of Stop
    objects.
    """
    def __init__(self):
        self.id = None
        self.name = None
        self.zone = None
        self.is_hub = False
        self.x = None
        self.y = None

        self.in_name = False
        self.in_zone = False
        self.in_is_hub = False
        self.in_x = False
        self.in_y = False
        self.in_id = False

        self.stops = []

    def set_all_none(self):
        self.id = None
        self.name = None
        self.zone = None
        self.is_hub = False
        self.x = None
        self.y = None

    def clear_flags(self):
        self.in_name = False
        self.in_zone = False
        self.in_is_hub = False
        self.in_x = False
        self.in_y = False
        self.in_id = False

    def startElement(self, name, attrs):
        if name == 'Name':
            self.in_name = True
        elif name == 'Zone':
            self.in_zone = True
        elif name == 'InHub':
            self.in_is_hub = True
        elif name == 'X':
            self.in_x = True
        elif name == 'Y':
            self.in_y = True
        elif name == 'ID':
            self.in_id = True

    def endElement(self, name):
        self.set_all_none()
        self.clear_flags()
        if name == 'Stop':
            s = Stop()
            s.x = self.x
            s.y = self.y
            s.id = self.id
            s.zone = self.zone
            s.is_hub = self.is_hub
            self.stops.append(s)

    def characters(self, content):
        if self.in_name:
            self.name = content
        elif self.in_is_hub:
            self.is_hub = (content == 'True')
        elif self.in_x:
            self.x = content
        elif self.in_y:
            self.y = content
        elif self.in_id:
            self.id = content