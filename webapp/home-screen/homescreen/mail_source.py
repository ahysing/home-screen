import paramiko
import requests
import requests_ntlm


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

    def parseCalendarResult(self):
        pass

    def lookupCalendarTo(self, date_str):
        # Set up the connection to Exchange
        session = requests.session()
        httml_ntlm_auth = requests_ntlm.HttpNtlmAuth(self.service_account_username, self.service_account_password)
        calendar = self.parseCalendarResult()
        return calendar
