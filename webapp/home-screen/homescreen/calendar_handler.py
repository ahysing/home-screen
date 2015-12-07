import xml.sax
import  logging

logger = logging.getLogger(__name__)

class ExchangeErroHandler(xml.sax.ContentHandler):
    def __init__(self):
        pass


    def startElement(self, name, attrs):
        if name == 'Error':
            self.in_error = True

    def endElement(self, name):
        if name == 'Error':
            end

class CalendarHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.calendar_list = []
        self.in_title = False


    def startElement(self, name, attrs):
        if name == 'Event':
            self.in_event = True


    def endElement(self, name):
        pass