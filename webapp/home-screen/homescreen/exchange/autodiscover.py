import pysimplesoap
import requests
import requests.exceptions
import logging
from . import config


logger = logging.getLogger(__name__)


autodiscoverGetUserSettingsRequestMessage = """\
<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:a="http://schemas.microsoft.com/exchange/2010/Autodiscover"
        xmlns:wsa="http://www.w3.org/2005/08/addressing"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Header>
    <a:RequestedServerVersion>Exchange2013</a:RequestedServerVersion>
    <wsa:Action>http://schemas.microsoft.com/exchange/2010/Autodiscover/Autodiscover/GetUserSettings</wsa:Action>
    <wsa:To>https://autodiscover.exchange.microsoft.com/autodiscover/autodiscover.svc</wsa:To>
  </soap:Header>
  <soap:Body>
    <a:GetUserSettingsRequestMessage xmlns:a="http://schemas.microsoft.com/exchange/2010/Autodiscover">
      <a:Request>
        <a:Users>
          <a:User>
            <a:Mailbox>mara@contoso.com</a:Mailbox>
          </a:User>
        </a:Users>
        <a:RequestedSettings>
          <a:Setting>UserDisplayName</a:Setting>
          <a:Setting>UserDN</a:Setting>
          <a:Setting>UserDeploymentId</a:Setting>
          <a:Setting>InternalMailboxServer</a:Setting>
          <a:Setting>MailboxDN</a:Setting>
          <a:Setting>PublicFolderServer</a:Setting>
          <a:Setting>ActiveDirectoryServer</a:Setting>
          <a:Setting>ExternalMailboxServer</a:Setting>
          <a:Setting>EcpDeliveryReportUrlFragment</a:Setting>
          <a:Setting>EcpPublishingUrlFragment</a:Setting>
          <a:Setting>EcpTextMessagingUrlFragment</a:Setting>
          <a:Setting>ExternalEwsUrl</a:Setting>
          <a:Setting>CasVersion</a:Setting>
          <a:Setting>EwsSupportedSchemas</a:Setting>
          <a:Setting>GroupingInformation</a:Setting>
        </a:RequestedSettings>
      </a:Request>
    </a:GetUserSettingsRequestMessage>
  </soap:Body>
</soap:Envelope>"""

# Autodiscover defines two standard endpoint URL forms that are derived from the domain portion of the user's email address:
def autodiscover(emailaddress):
    domain = emailaddress.split("@", 1)[1]

    auth = (config.USERNAME, config.PASSWORD)
    for endpoint in ["https://" + domain + "/autodiscover/autodiscover.svc",
                     "https://autodiscover." + domain + "/autodiscover/autodiscover.svc"]:
        logger.info("Trying endpoint '%s'" % (endpoint,))
        try:
            response = requests.get(endpoint, auth=auth)
            logger.info("response.status_code: %s\nresponse.text: %s" % (response.status_code, response.text))

            if response.status_code == 200:
                response = requests.post(endpoint,
                                         data=autodiscoverGetUserSettingsRequestMessage,
                                         auth=auth)
                logger.info("getusersettings response.status_code: %s\nresponse.text: %s" % (response.status_code, response.text))


        except requests.exceptions.ConnectionError:
            logger.info("Failed to connect to the endpoint '%s'" % (endpoint,))
            pass


#The value of fileExtension depends on which Autodiscover access method you are using, SOAP or POX. The SOAP service uses a ".svc" file extension; POX uses ".xml".

#"https://" + domain + "/autodiscover/autodiscover" + fileExtension
#"https://autodiscover." + domain + "/autodiscover/autodiscover" + fileExtension



