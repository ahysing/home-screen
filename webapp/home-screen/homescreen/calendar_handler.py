import xml.sax
import  logging

logger = logging.getLogger(__name__)


class CalendarHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.calendar_list = []
        self.in_title = False

    def startElement(self, name, attrs):
        pass


    def endElement(self, name):
        pass