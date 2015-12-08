# -*- coding: utf-8 -*-
from pyramid.response import Response
from pyramid.view import view_config
import input_validation
import zip_place_source
import weather_source
import public_transport_source
from public_transport_source import RuterException
from .mail_source import MailSource, MsExchangeException
from .weather_source import YrException
import datetime
import traceback
import logging

logger = logging.getLogger(__name__)


@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    one = 'one'
    return {'one': one, 'project': 'home-screen'}

def build_error_latlong(latitude, longitude):
    return 'location not accepted latitude={0} longitude={1}'.format(latitude, longitude)


@view_config(route_name='transport:next:static', renderer='templates/transport_next_static.pt')
def transport_next_static(request):
    alt_departure_type = 'Transportmiddel for avreise'
    error = None
    from_dt = '2015-01-01T00:00:00Z'
    from_time = '00:00'
    latitude = u'59.5440'         # Longitude and latitude for the center of Oslo
    limit, error = _parse_limit_or_error(request)
    longitude = u'10.4510'        # Longitude and latitude for the center of Oslo
    stop_name = 'Oslo S'
    transport = None
    updated = '2015-01-01T00:00:00Z'
    updated_txt = 'Sist oppdatert'

    if 'latitude' in request.GET and 'longitude' in request.GET:
        latitude = request.GET['latitude']
        longitude = request.GET['longitude']

    try:
        logger.debug('transport_next latitude={0} longitude={1}'.format(latitude, longitude))
        transport = public_transport_source.lookup_transport_for_stop(latitude, longitude, limit=limit)
    except RuterException as e:
        error = str(e)
        logger.error(str(e))
    return {'from':from_dt, 'from_time':from_time, 'alt_departure_type': alt_departure_type,
            'updated_txt': updated_txt, 'updated':updated, 'stop_name':stop_name,
            'transport': transport, 'error':error}

def _parse_limit_or_error(request):
    limit = 10
    error = None
    try:
        limit = request.GET['limit']
        limit = max(1, int(limit))
    except KeyError:
        pass
    except ValueError:
        error = 'Invalid limit sent to service. Expected integer got {}'.format(limit)
    return limit, error

@view_config(route_name='transport:next', renderer='json')
def transport_next(request):
    error = None
    try:
        if 'latitude' in request.GET and 'longitude' in request.GET:
            latitude = request.GET['latitude']
            longitude = request.GET['longitude']
            limit, error = _parse_limit_or_error(request)
            if not input_validation.is_valid_wgs_84(latitude, longitude):
                request.response.status = 400
                return {'error': build_error_latlong(latitude, longitude), 'params': ['latitude', 'longitude']}
            else:
                if type(limit) == int:
                    logger.debug('transport_next latitude={0} longitude={1} limit={2}'.format(latitude, longitude, limit))
                    transport = public_transport_source.lookup_transport_for_stop(latitude, longitude, limit=limit)
                else:
                    logger.debug('transport_next latitude={0} longitude={1}'.format(latitude, longitude))
                    transport = public_transport_source.lookup_transport_for_stop(latitude, longitude)
                return {'error': error, 'transport': transport}
        else:
            return {'info': 'Pass parameters latitude, longitude. \
The response is the next public transport departures. Optionally pass limit for fewer items.',
                    'params': ['latitude', 'longitude', 'limit']}
    except RuterException as e:
        logger.error(traceback.print_exc())
        message = str(e)
        request.response.status = 500
        return {'error': message, 'params': ['latitude', 'longitude', 'limit']}


@view_config(route_name='forecast:static', renderer='templates/forecast_static.pt')
def forecast_static(request):
    dt_separator = 'til'
    error = None
    forecast = None
    from_dt = '2015-01-01T00:00:00Z'
    from_time = '00:00'
    icon = 'wi'
    postnummer = '0250' # Aker Brygge per november 2015
    temperature = '0'
    to_dt = '2015-01-01T00:00:00Z'
    to_time = '00:00'
    weather_h1 = 'Været for Oslo'
    if 'postnummer' in request.GET:
            postnummer = request.GET['postnummer']
            if not input_validation.is_valid_postnummer(postnummer):
                request.response.status = 400
                return {'error': 'postnummer not accepted', 'params': ['postnummer']}

    try:
        forecast = weather_source.lookup_forecast_for_postnummer(postnummer)
    except YrException as e:
	    error = str(e)
        logger.error(str(e))
    return {'icon': icon, 'temperature': temperature, 'dt_separator': dt_separator, 'forecast':forecast, 'from':from_dt,
            'to':to_dt, 'from_time': from_time, 'to_time': to_time, 'weather_h1': weather_h1, 'error': error}

@view_config(route_name='forecast', renderer='json')
def forecast(request):
    try:
        if 'postnummer' in request.GET:
            postnummer = request.GET['postnummer']
            if not input_validation.is_valid_postnummer(postnummer):
                request.response.status = 400
                return {'error': 'postnummer not accepted', 'params': ['postnummer']}
            else:
                forecast = weather_source.lookup_forecast_for_postnummer(postnummer)
                return {'error': None, 'forecast': forecast}
        if 'latitude' in request.GET and 'longitude' in request.GET:
            latitude = request.GET['latitude']
            longitude = request.GET['longitude']
            if not input_validation.is_valid_wgs_84(latitude, longitude):
                request.response.status = 400
                return {'error': build_error_latlong(latitude, longitude), 'params': ['latitude', 'longitude']}
            else:
                postnummer = zip_place_source.lookup_postnummer_closest_to(latitude, longitude)
                forecast = weather_source.lookup_forecast_for_postnummer(postnummer)
                return {'error': None, 'forecast': forecast}
        elif len(request.params) > 0:
            request.response.status = 400
            return {'error': 'Missing parameters', 'params': ['postnummer', 'latitude', 'longitude']}
        else:
            return {'info': 'Pass parameters postnummer from posten or a pair of latitude, longitude.\
The response is the current weather forecast', 'params': ['postnummer', 'latitude', 'longitude']}
    except YrException as e:
        message = str(e)
        request.response.status = 500
        return {'error': message, 'params': ['postnummer', 'latitude', 'longitude']}

def _get_next_week_date():
    end = datetime.datetime.now() + datetime.timedelta(days=7)
    return end

@view_config(route_name='mail:calendar', renderer='json')
def mail_calendar(request):
    message = None
    root_url = 'https://mail.bouvet.no/autodiscover/autodiscover.xml'
    end = _get_next_week_date()
    try:
        mail_source = MailSource(root_url)
        calendar = mail_source.lookup_calendar_to(end)
        return {'error': message, 'params': [], 'result': calendar}
    except MsExchangeException as e:
        message = str(e)
        request.response_status = 500
        return {'error': message, 'params': [], 'result': None}

@view_config(route_name='index', renderer='templates/index.pt')
def index(request):
    root_url = 'https://mail.bouvet.no/autodiscover/autodiscover.xml'
    try:
        return { 'mail_url' :  root_url, 'params': [], 'calendar': None, 'show_authenticate': 'active-form' }
    except Exception as e:
        message = str(e)
        request.response.status = 500
        return {'error': message, 'params': [], 'calendar': None,'show_authenticate': ''}

#TODO: this view is not programmed yet
@view_config(route_name='index:static', renderer='templates/index.pt')
def index_static(request):
    end = _get_next_week_date()
    root_url = 'https://mail.bouvet.no/autodiscover/autodiscover.xml'
    username = ''
    password = ''
    try:
        mail_source = MailSource(root_url, service_account_username=username, service_account_password=password)
        calendar = mail_source.lookup_calendar_to(end)
        return { 'mail_url' : root_url, 'calendar': calendar, 'show_authenticate': 'active-form' }
    except MsExchangeException as e:
        message = str(e)
        request.response.status = 500
        return {'error': message, 'params': [], 'calendar': None, 'show_authenticate': ''}

@view_config(route_name='index:authenticate', renderer='templates/index.pt')
def index_authenticate(request):
    message = None
    username = request.params['username']
    password = request.params['password']
    root_url = 'https://mail.bouvet.no/autodiscover/autodiscover.xml'
    end = _get_next_week_date()
    try:
        mail_source = MailSource(root_url, service_account_username=username, service_account_password=password)
        calendar = mail_source.lookup_calendar_to(end)
        return {'error': message, 'params': ['username', 'password'], 'calendar': calendar, 'show_authenticate': 'inactive-form'}
    except MsExchangeException as e:
        message = str(e)
        request.response.status = 500
        return {'error': message, 'params': ['username', 'password'], 'calendar': None, 'show_authenticate': 'active-form'}

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_home-screen_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
