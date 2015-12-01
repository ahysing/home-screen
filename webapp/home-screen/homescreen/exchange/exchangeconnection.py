import asyncio
import copy
import logging
import pprint
import ssl
from lxml import etree

import io

import re
from ntlm3 import ntlm

from . import asyncioutils
from . import utils

logger = logging.getLogger(__name__)


subscribe_to_tasks_message = """\
<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
  xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types">
  <soap:Header>
    <t:ExchangeImpersonation>
      <t:ConnectingSID>
        <t:PrimarySmtpAddress>%(user_email_address)s</t:PrimarySmtpAddress>
      </t:ConnectingSID>
    </t:ExchangeImpersonation>
    <t:RequestServerVersion Version="Exchange2010_SP1"/>
  </soap:Header>
  <soap:Body>
    <Subscribe xmlns="http://schemas.microsoft.com/exchange/services/2006/messages">
      <StreamingSubscriptionRequest>
        <t:FolderIds>
          <t:DistinguishedFolderId Id="tasks"/>
        </t:FolderIds>
        <t:EventTypes>
          <t:EventType>CreatedEvent</t:EventType>
          <t:EventType>ModifiedEvent</t:EventType>
          <t:EventType>MovedEvent</t:EventType>
          <t:EventType>DeletedEvent</t:EventType>
        </t:EventTypes>
      </StreamingSubscriptionRequest>
    </Subscribe>
  </soap:Body>
</soap:Envelope>"""


get_streaming_events_msg = """\
<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
  xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types"
  xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages">
  <soap:Header>
    <t:ExchangeImpersonation>
      <t:ConnectingSID>
        <t:PrimarySmtpAddress>%(user_email_address)s</t:PrimarySmtpAddress>
      </t:ConnectingSID>
    </t:ExchangeImpersonation>
    <t:RequestServerVersion Version="Exchange2010_SP1"/>
  </soap:Header>
  <soap:Body>
    <GetStreamingEvents xmlns="http://schemas.microsoft.com/exchange/services/2006/messages">
      <SubscriptionIds>
        <t:SubscriptionId>%(subscription_id)s</t:SubscriptionId>
      </SubscriptionIds>
      <ConnectionTimeout>30</ConnectionTimeout>
    </GetStreamingEvents>
  </soap:Body>
</soap:Envelope>"""


find_tasks_message = """\
<x:Envelope xmlns:x="http://schemas.xmlsoap.org/soap/envelope/" xmlns:mes="http://schemas.microsoft.com/exchange/services/2006/messages" xmlns:typ="http://schemas.microsoft.com/exchange/services/2006/types">
  <x:Header>
    <typ:ExchangeImpersonation>
      <typ:ConnectingSID>
        <typ:PrimarySmtpAddress>%(user_email_address)s</typ:PrimarySmtpAddress>
      </typ:ConnectingSID>
    </typ:ExchangeImpersonation>
    <typ:RequestServerVersion Version="Exchange2010_SP1"/>
  </x:Header>
  <x:Body>
    <mes:FindItem Traversal="Shallow">
      <mes:ItemShape>
        <!-- typ:BaseShape>Default</typ:BaseShape-->
        <typ:BaseShape>AllProperties</typ:BaseShape>
        <typ:ConvertHtmlCodePageToUTF8>true</typ:ConvertHtmlCodePageToUTF8>
      </mes:ItemShape>
      <mes:IndexedPageItemView MaxEntriesReturned="2" Offset="%(indexed_page_offset)d" BasePoint="Beginning"/>
      <mes:ParentFolderIds>
        <typ:DistinguishedFolderId Id="tasks"/>
      </mes:ParentFolderIds>
    </mes:FindItem>
  </x:Body>
</x:Envelope>"""


create_task_message = """\
<x:Envelope xmlns:x="http://schemas.xmlsoap.org/soap/envelope/" xmlns:mes="http://schemas.microsoft.com/exchange/services/2006/messages" xmlns:typ="http://schemas.microsoft.com/exchange/services/2006/types">
  <x:Header>
    <typ:ExchangeImpersonation>
      <typ:ConnectingSID>
        <typ:PrimarySmtpAddress>%(user_email_address)s</typ:PrimarySmtpAddress>
      </typ:ConnectingSID>
    </typ:ExchangeImpersonation>
    <typ:RequestServerVersion Version="Exchange2010_SP1"/>
  </x:Header>
  <x:Body>
    <mes:CreateItem>
      <mes:SavedItemFolderId>
        <typ:DistinguishedFolderId Id="tasks"/>
      </mes:SavedItemFolderId>
      <mes:Items>
        <typ:Task>
          <typ:Subject>%(subject)s</typ:Subject>
          <typ:Body BodyType="Text"> %(subject)s</typ:Body>
        </typ:Task>
      </mes:Items>
    </mes:CreateItem>
  </x:Body>
</x:Envelope>"""


delete_item_message = """\
<x:Envelope xmlns:x="http://schemas.xmlsoap.org/soap/envelope/" xmlns:mes="http://schemas.microsoft.com/exchange/services/2006/messages" xmlns:typ="http://schemas.microsoft.com/exchange/services/2006/types">
  <x:Header>
    <typ:ExchangeImpersonation>
      <typ:ConnectingSID>
        <typ:PrimarySmtpAddress>%(user_email_address)s</typ:PrimarySmtpAddress>
      </typ:ConnectingSID>
    </typ:ExchangeImpersonation>
    <typ:RequestServerVersion Version="Exchange2010_SP1"/>
  </x:Header>
  <x:Body>

  <mes:DeleteItem DeleteType="HardDelete" AffectedTaskOccurrences="AllOccurrences">
    <mes:ItemIds>
      <typ:ItemId Id="%(item_id)s"/>
    </mes:ItemIds>
  </mes:DeleteItem>

  </x:Body>
</x:Envelope>"""


class MSExchangeConnectionError(Exception):
    pass


class MSExchangeConnection:
    """Each instance of this class is to represents one tcp connection to the exchange server. Each connection
    represents one exchange user.

    We want a nice api for handling a ntml-authenticated connection to the exchange server and getting
    events for a user.
    """
    def __init__(self, msexchange_server, user_email_address):
        self._msexchange_server = msexchange_server
        self.user_email_address = user_email_address
        self._is_closed = False
        self._reader = None
        self._writer = None
        self._cookies = None

    _ssl_context = ssl._create_default_https_context()
    _ssl_context.check_hostname = False
    _ssl_context.verify_mode = ssl.CERT_NONE

    def __enter__(self):
        return self

    def __exit__(self, *exs):
        try:
            self.close()
            if self._msexchange_server.user_email_address2connection.get(self.user_email_address) is self:
                del self._msexchange_server.user_email_address2connection[self.user_email_address]
        except Exception as e:
            pass
        return False

    def get_tasks_sync(self):
        tasks = asyncio.get_event_loop().run_until_complete(self.get_tasks())
        return tasks

    @asyncio.coroutine
    def get_tasks(self):
        results = []
        # The searchresults might be paged, so we may have to send more than one request to the server to get
        # all the results.
        indexed_page_offset = 0
        has_got_all_results = False
        while not has_got_all_results:
            msg = find_tasks_message % dict(
                user_email_address=self.user_email_address,
                indexed_page_offset=indexed_page_offset)
            headers = dict(SOAPAction="http://schemas.microsoft.com/exchange/services/2006/messages/FindItem")
            response, content = yield from self._send_request(method="POST",
                                                              request_headers=headers,
                                                              data=msg)

            if response.status != 200:
                raise MSExchangeConnectionError("get_tasks() failed! response.status:%s content:\n%s" % (
                    response.status, content))

            root = etree.parse(io.BytesIO(content))  # surely there has to be a simpler way of parsing a bytearray?

            find_item_response_message = root.find(
                ".//{http://schemas.microsoft.com/exchange/services/2006/messages}FindItemResponseMessage")
            if find_item_response_message is None:
                raise MSExchangeConnectionError(
                    "Didn't find the 'FindItemResponseMessage' element in the response! response-content:\n%s" % (
                        content,))

            root_folder = find_item_response_message.find(
                "{http://schemas.microsoft.com/exchange/services/2006/messages}RootFolder")

            if find_item_response_message is None:
                raise MSExchangeConnectionError(
                    "Didn't find the 'RootFolder' element in the response! response-content:\n%s" % (
                        content,))

            response_class = find_item_response_message.get("ResponseClass")
            if response_class != "Success":
                raise MSExchangeConnectionError(
                    "The FindItem request failed with ResponseClass '%s'! response-content:\n%s" % (
                        response_class, content,))

            response_code = root.findtext(".//{http://schemas.microsoft.com/exchange/services/2006/messages}ResponseCode")
            if response_code != "NoError":
                raise MSExchangeConnectionError("get_tasks() failed (response_code:'%s')! response.status:%s content:\n%s" % (
                    response_code,
                    response.status, content))

            # Check if this is the last page of the searchresults
            if root_folder.get("IncludesLastItemInRange") == "true":
                # Yep, this was the last page
                has_got_all_results = True
            else:
                # This was not the last page, so continue with the new offset
                indexed_page_offset = int(root_folder.get("IndexedPagingOffset"))

            items = root_folder.find("{http://schemas.microsoft.com/exchange/services/2006/types}Items")
            if items is None:
                raise MSExchangeConnectionError(
                    "Didn't find the 'Items' element in the response! response-content:\n%s" % (
                        content,))

            for item in items:
                # The item looks something like this:
                #  <t:Task>
                #    <t:ItemId Id="AQMkADAzNmNhNjJkLWViN2MtNGI2Mi04MzIzLTYwNDI3YmUzOWUxYQBGAAADnXryXV+8zkWj87Fi5hRdvwcA+U0/XFL4WEGRsdue41137QAAAgESAAAA+U0/XFL4WEGRsdue41137QAAAhEMAAAA" ChangeKey="EwAAABYAAAD5TT9cUvhYQZGx257jXXftAAAEGQCo"/>
                #    <t:Subject>Order new brakes</t:Subject>
                #    <t:HasAttachments>false</t:HasAttachments>
                #    <t:PercentComplete>0</t:PercentComplete>
                #    <t:Status>NotStarted</t:Status>
                #  </t:Task>
                # We want to flatten this into a dict like this:
                # {"itemtype": "Task",
                #  "ItemId": AQMkADAzNmNhNjJkLWViN2MtNGI2Mi04MzIzLTYwNDI3YmUzOWUxYQBGAAADnXryXV+8zkWj87Fi5hRdvwcA+U0/XFL4WEGRsdue41137QAAAgESAAAA+U0/XFL4WEGRsdue41137QAAAhEMAAAA" ChangeKey="EwAAABYAAAD5TT9cUvhYQZGx257jXXftAAAEGQCo",
                #  "Subject": "Order new brakes",
                #  "HasAttachments": "false",
                #  "PercentComplete": "0",
                #  "Status": "NotStarted"
                #  }
                iteminfo = dict(item.attrib)
                iteminfo["itemtype"] = utils.remove_namespace(item.tag)
                for child in item:
                    valuename = utils.remove_namespace(child.tag)
                    value = child.text
                    if not value:
                        if child.get("Id"):
                            value = child.get("Id")
                        else:
                            value = dict(child.attrib)
                    iteminfo[valuename] = value
                results.append(iteminfo)

        return results

    def create_task_sync(self, subject, body):
        task_id = asyncio.get_event_loop().run_until_complete(self.create_task(subject, body))
        return task_id

    @asyncio.coroutine
    def create_task(self, subject, body):
        msg = create_task_message % dict(user_email_address=self.user_email_address,
                                         subject=subject,
                                         body=body)
        headers = dict(SOAPAction="http://schemas.microsoft.com/exchange/services/2006/messages/CreateItem")
        response, content = yield from self._send_request(method="POST",
                                                          request_headers=headers,
                                                          data=msg)

        if response.status != 200:
            raise MSExchangeConnectionError("create_task() failed! response.status:%s content:\n%s" % (
                response.status, content))

        root = etree.parse(io.BytesIO(content))  # surely there has to be a simpler way of parsing a bytearray?

        create_item_response_message = root.find(
            ".//{http://schemas.microsoft.com/exchange/services/2006/messages}CreateItemResponseMessage")
        if create_item_response_message is None:
            raise MSExchangeConnectionError(
                "Didn't find the 'CreateItemResponseMessage' element in the response! response-content:\n%s" % (
                    content,))

        response_class = create_item_response_message.get("ResponseClass")
        if response_class != "Success":
            raise MSExchangeConnectionError(
                "The CreateItem request failed with ResponseClass '%s'! response-content:\n%s" % (
                    response_class, content,))

        response_code = create_item_response_message.findtext(
            ".//{http://schemas.microsoft.com/exchange/services/2006/messages}ResponseCode")
        if response_code != "NoError":
            raise MSExchangeConnectionError(
                "create_item() failed (response_code:'%s')! response.status:%s content:\n%s" % (
                    response_code,
                    response.status, content))

        item_id = create_item_response_message.find(".//{http://schemas.microsoft.com/exchange/services/2006/types}ItemId").get("Id")
        return item_id

    def delete_item_sync(self, item_id):
        asyncio.get_event_loop().run_until_complete(self.delete_item(item_id))

    @asyncio.coroutine
    def delete_item(self, item_id):
        msg = delete_item_message % dict(user_email_address=self.user_email_address,
                                         item_id=item_id)
        headers = dict(SOAPAction="http://schemas.microsoft.com/exchange/services/2006/messages/DeleteItem")
        response, content = yield from self._send_request(method="POST",
                                                          request_headers=headers,
                                                          data=msg)

        if response.status != 200:
            raise MSExchangeConnectionError("delete_item() failed! response.status:%s content:\n%s" % (
                response.status, content))

        root = etree.parse(io.BytesIO(content))  # surely there has to be a simpler way of parsing a bytearray?

        delete_item_response_message = root.find(
            ".//{http://schemas.microsoft.com/exchange/services/2006/messages}DeleteItemResponseMessage")
        if delete_item_response_message is None:
            raise MSExchangeConnectionError(
                "Didn't find the 'DeleteItemResponseMessage' element in the response! response-content:\n%s" % (
                    content,))

        response_class = delete_item_response_message.get("ResponseClass")
        if response_class != "Success":
            raise MSExchangeConnectionError(
                "The DeleteItem request failed with ResponseClass '%s'! response-content:\n%s" % (
                    response_class, content,))

        response_code = delete_item_response_message.findtext(
            ".//{http://schemas.microsoft.com/exchange/services/2006/messages}ResponseCode")
        if response_code != "NoError":
            raise MSExchangeConnectionError(
                "delete_item() failed (response_code:'%s')! response.status:%s content:\n%s" % (
                    response_code,
                    response.status, content))

    @asyncio.coroutine
    def smoke_test_get_request(self):
        try:
            for requestindex in range(10):
                response, content = yield from self._send_request(method="GET")
                if not response.status == 200:
                    raise AssertionError("smoketest#%d failed! response.status:%s" % (requestindex, response.status,))
                #logger.info("request#%d succeeded" % (requestindex,))

        finally:
            if self._writer is not None:
                self._writer.close()
        return response, content

    def close(self):
        self._is_closed = True
        if self._writer is not None:
            self._writer.close()

    @asyncio.coroutine
    def poll_for_events(self, result_queue):
        while not self._is_closed:
            try:
                subscription_id = yield from self.send_subscribe_request()
                if not subscription_id:
                    logger.warning("Failed to get a subscription for the user '%s'. I'll retry later." % (self.user_email_address,))
                else:
                    logger.debug("poll_for_events(): calling send_sync_request()")
                    yield from self.send_sync_request(subscription_id, result_queue) # this hangs until the connection is lost of the subscription expires
            except:
                logger.exception("Something went wrong, but I'll retry in a while")

    @asyncio.coroutine
    def send_subscribe_request(self):
        msg = subscribe_to_tasks_message % dict(user_email_address=self.user_email_address)
        headers = dict(SOAPAction="http://schemas.microsoft.com/exchange/services/2006/messages/Subscribe")
        response, content = yield from self._send_request(method="POST",
                                                          request_headers=headers,
                                                          data=msg)

        if response.status != 200:
            logger.warning("send_subscribe_request() failed! response.status:%s content:\n%s" % (
                response.status, content))
            return None

        root = etree.parse(io.BytesIO(content))  # surely there has to be a simpler way of parsing a bytearray?
        response_code = root.findtext(".//{http://schemas.microsoft.com/exchange/services/2006/messages}ResponseCode")
        if response_code != "NoError":
            logger.warning("send_subscribe_request() failed (response_code:'%s')! response.status:%s content:\n%s" % (
                response_code,
                response.status, content))
            return None

        subscription_id = root.findtext(".//{http://schemas.microsoft.com/exchange/services/2006/messages}SubscriptionId")
        if not subscription_id:
            logger.warning("send_subscribe_request() didn't contain a SubscriptionId! response.status:%s content:\n%s" % (
                response_code,
                response.status, content))
            return None
        return subscription_id

    @asyncio.coroutine
    def send_sync_request(self, subscription_id, event_queue):
        msg = get_streaming_events_msg % dict(subscription_id=subscription_id,
                                              user_email_address=self.user_email_address)
        headers = dict(SOAPAction="http://schemas.microsoft.com/exchange/services/2006/messages/GetEvents")

        class ParserTarget:
            def __init__(self, the_event_queue, default_event_values):
                self.open_tags_stack = []
                self.currentGetStreamingEventsResponseMessage = None
                self.currentNotifications = []
                self.event_queue = the_event_queue
                self.default_event_values = default_event_values

            def start(self, tag, attrib):
                if tag == "dummyrootelement":
                    return
                attrib = dict(attrib)
                logger.debug("ParserTarget.start() tag:'%s'  attrib='%s'" % (tag, attrib))
                taginfo = dict(tag=tag, attrib=attrib, children=[])
                if len(self.open_tags_stack) > 0:
                    # This is not the root tag, so add it as a child of the currently open tag
                    current_tag = self.open_tags_stack[-1]
                    current_tag["children"].append(taginfo)
                self.open_tags_stack.append(taginfo)

                if tag == '{http://schemas.xmlsoap.org/soap/envelope/}Envelope':
                    logger.debug("ParserTarget.start() A new message is starting")

                elif tag == "{http://schemas.microsoft.com/exchange/services/2006/messages}GetStreamingEventsResponseMessage":
                    self.currentGetStreamingEventsResponseMessage = taginfo

                elif tag == "{http://schemas.microsoft.com/exchange/services/2006/messages}Notification":
                    self.currentNotifications.append(taginfo)

            def end(self, tag):
                logger.debug("ParserTarget.end() tag:'%s'  len(self.open_tags_stack):%s" % (
                    tag, len(self.open_tags_stack)))
                taginfo = self.open_tags_stack.pop()
                if len(self.open_tags_stack) == 0:
                    logger.debug("ParserTarget.end() We have got a complete message, so handle it now. message:\n%s" % (
                        pprint.pformat(taginfo),
                    ))
                    try:
                        status = self.currentGetStreamingEventsResponseMessage["attrib"]["ResponseClass"]
                        if status != "Success":
                            raise MSExchangeConnectionError(
                                'The GetStreamingEventsResponseMessage-message for the user "%s" failed! status:"%s"' %
                                (status,))
                        else:
                            logger.debug("ParserTarget.end() the message looks ok.")

                        for notification in self.currentNotifications:
                            for event in notification["children"]:
                                tagname = utils.remove_namespace(event["tag"])
                                if tagname == 'SubscriptionId':
                                    continue  # this is just metadata. skip it.
                                eventinfo = copy.copy(self.default_event_values)
                                eventinfo["EventType"] = tagname
                                for childtaginfo in event["children"]:
                                    valuename = utils.remove_namespace(childtaginfo["tag"])
                                    if "data" in childtaginfo:
                                        eventinfo[valuename] = childtaginfo["data"]
                                    else:
                                        if valuename in ["ItemId", "ParentFolderId"]:
                                            eventinfo[valuename] = childtaginfo["attrib"]["Id"]
                                        else:
                                            eventinfo[valuename] = childtaginfo["attrib"]

                                logger.debug("ParserTarget.end() generated an event: %s" % (pprint.pformat(eventinfo),))

                                self.event_queue.put_nowait(eventinfo)

                    finally:
                        self.currentGetStreamingEventsResponseMessage = None
                        self.currentNotifications = []

            def data(self, data):
                logger.debug("ParserTarget.data() data:'%s'" % (data, ))
                if len(self.open_tags_stack) > 0:
                    currenttag = self.open_tags_stack[-1]
                    currenttag["data"] = data

            def comment(self, text):
                logger.debug("ParserTarget.comment() text:'%s'" % (text, ))

            def close(self):
                logger.info("ParserTarget.close()")

        parser_target = ParserTarget(event_queue,
                                     default_event_values=dict(user_email_address=self.user_email_address,
                                                               ms_exchange_connection=self))

        chunked_data_parser = etree.XMLParser(target=parser_target)
        chunked_data_parser.feed(b"<dummyrootelement>")

        response, content = yield from self._send_request(method="POST", request_headers=headers, data=msg,
                                                          chunked_data_handler=chunked_data_parser.feed)

        if response.status != 200:
            logger.info("send_sync_request() failed! response.status:%s content:\n%s" % (
                response.status, content))
            return None

        root = etree.parse(io.BytesIO(content))  # surely there has to be a simpler way of parsing a bytearray?
        response_code = root.findtext(".//{http://schemas.microsoft.com/exchange/services/2006/messages}ResponseCode")
        if response_code != "NoError":
            logger.info("send_sync_request() failed (response_code:'%s')! response.status:%s content:\n%s" % (
                response_code,
                response.status, content))
            return None

        events = [] # TODO
        return events


    _asyncio_test_run_count = 0

    @asyncio.coroutine
    def _send_request(self, method="POST", request_headers=None, data=None, chunked_data_handler=None):
        """Utilitymethod for sending a request (and authenticating with ntml if we are not already authenticated).
        """
        logger.debug("_send_request() starting")

        url = self._msexchange_server.exchange_server_url

        # logger.info("_send_request() starting")
        if not request_headers:
            request_headers = {}
        else:
            request_headers = copy.copy(request_headers)

        if self._reader is None:
            # We don't have a tcp connection, so create one now
            logger.debug("_send_request() calling asyncio.open_connection()")
            reader, writer = yield from asyncio.open_connection(
                self._msexchange_server.exchange_server_ip, self._msexchange_server.exchange_server_port,
                ssl=self._ssl_context)
            logger.debug("_send_request() finished calling asyncio.open_connection()")
            self._reader = reader
            self._writer = writer
        else:
            # We have an existing (possibly already authenticated) connection, so add any cookies to the
            # request.
            reader = self._reader
            writer = self._writer
            if self._cookies:
                request_headers["Cookie"] = self._cookies

        logger.debug("_send_request() calling asyncioutils.async_http_request()")
        response, content = yield from asyncioutils.async_http_request(reader, writer, url,
                                                                       request_headers, method=method,
                                                                       data=data,
                                                                       chunked_data_handler=chunked_data_handler)
        logger.debug("_send_request() done calling asyncioutils.async_http_request()")

        www_authenticate = [value.lower() for value in response.headers.get_all('www-authenticate', [])]

        if response.status == 401 and 'ntlm' in www_authenticate:
            auth_header_field = 'www-authenticate'
            auth_header = 'Authorization'
        else:
            proxy_authenticate = response.headers.get('proxy-authenticate', '').lower()
            if response.status == 407 and 'ntlm' in proxy_authenticate:
                auth_header_field = 'proxy-authenticate'
                auth_header = 'Proxy-authorization'

            else:
                # This response is already authenticated
                return response, content

        if auth_header in request_headers:
            # This request is already authenticated
            return response, content

        # Attempt to authenticate using HTTP NTLM challenge/response
        self.password = self._msexchange_server.service_account_password

        # parse the username
        try:
            self.domain, self.username = self._msexchange_server.service_account_username.split('\\', 1)
        except ValueError:
            raise ValueError(
                r"username should be in 'domain\\username' format."
            )

        self.domain = self.domain.upper()


        # initial auth header with username. will result in challenge
        msg = "%s\\%s" % (self.domain, self.username) if self.domain else self.username

        # ntlm returns the headers as a base64 encoded bytestring. Convert to
        # a string.
        auth = 'NTLM %s' % ntlm.create_NTLM_NEGOTIATE_MESSAGE(msg).decode('ascii')
        request2_headers = copy.copy(request_headers)
        request2_headers[auth_header] = auth

        # A streaming response breaks authentication.
        # This can be fixed by not streaming this request, which is safe
        # because the returned response3 will still have stream=True set if
        # specified in args. In addition, we expect this request to give us a
        # challenge and not the real content, so the content will be short
        # anyway.
        #args_nostream = dict(args, stream=False)
        #response2 = response.connection.send(request, **args_nostream)
        response2, content2 = yield from asyncioutils.async_http_request(reader, writer, url, request2_headers,
                                                                         method=method,
                                                                         data=data,
                                                                         chunked_data_handler=chunked_data_handler)

        # needed to make NTLM auth compatible with requests-2.3.0

        # Consume content and release the original connection
        # to allow our new request to reuse the same one.
        #response2.content
        #response2.raw.release_conn()
        request3_headers = copy.copy(request2_headers)

        # this is important for some web applications that store
        # authentication-related info in cookies (it took a long time to
        # figure out)
        if response2.headers.get('set-cookie'):
            request3_headers['Cookie'] = response2.headers.get_all('set-cookie')

        # get the challenge
        auth_header_value = response2.headers[auth_header_field]

        ntlm_header_value = list(filter(
            lambda s: s.startswith('NTLM '), auth_header_value.split(',')
        ))[0].strip()
        ServerChallenge, NegotiateFlags = ntlm.parse_NTLM_CHALLENGE_MESSAGE(
            ntlm_header_value[5:]
        )

        # build response

        # ntlm returns the headers as a base64 encoded bytestring. Convert to a
        # string.
        auth = 'NTLM %s' % ntlm.create_NTLM_AUTHENTICATE_MESSAGE(
            ServerChallenge, self.username, self.domain, self.password,
            NegotiateFlags
        ).decode('ascii')
        request3_headers[auth_header] = auth

        response3, content3 = yield from asyncioutils.async_http_request(reader, writer, url, request3_headers,
                                                                         method=method,
                                                                         data=data,
                                                                         chunked_data_handler=chunked_data_handler)

        return response3, content3


