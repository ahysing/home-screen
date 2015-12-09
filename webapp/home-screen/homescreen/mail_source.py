import requests
import requests_ntlm
import cStringIO
import xml.sax
import logging
from .calendar_handler import CalendarHandler

logger = logging.getLogger(__name__)


class MsExchangeException(Exception):
    pass


class MailSource(object):
    def __init__(self,
                 service_account_username="sesam-ci\srv_sesam",
                 service_account_password="Testing123.",
                 exchange_server_url="https://sesam-ci-xch.cloudapp.net/ews/exchange.asmx",
                 exchange_server_host="sesam-ci-xch.cloudapp.net",
                 exchange_server_port=443
                 ):
        self.service_account_username = service_account_username
        self.service_account_password = service_account_password
        self.exchange_server_url = exchange_server_url
        self.exchange_server_host = exchange_server_host
        self.exchange_server_port = exchange_server_port

    def parse_calendar_result(self, raw, content_type):
        try:
            calendar_handler = CalendarHandler()
            xml_reader = xml.sax.create_parser()
            xml_reader.setContentHandler(calendar_handler)
            stream = cStringIO.StringIO(raw)
            xml_reader.parse()
            xml_reader.close()
            return calendar_handler.calendar_list
        except xml.sax.SAXParseException as e:
            raise MsExchangeException(e)

    def lookup_calendar_to(self, date_str):
        # Set up the connection to Exchange
        session = requests.session()
        httml_ntlm_auth = requests_ntlm.HttpNtlmAuth(self.service_account_username, self.service_account_password)
        raw = ''
        content_type = ''
        calendar = self.parse_calendar_result(raw, content_type)
        return calendar
