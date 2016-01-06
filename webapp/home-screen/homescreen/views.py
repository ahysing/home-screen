# -*- coding: utf-8 -*-
import sys
import dateutil.parser
from time_utils import TimeUtils
from webutils import http_date
from pyramid.view import view_config, notfound_view_config
import input_validation
from .zip_place_source import lookup_postnummer_closest_to
import public_transport_source
from public_transport_source import RuterException
from .mail_source import MailSource, MsExchangeException
from .weather_source import lookup_forecast_for_postnummer, YrException
import datetime
import traceback
import logging

logger = logging.getLogger(__name__)
TIME_ZONE = 'Europe/Oslo'


@notfound_view_config(renderer = 'templates/not_found.pt')
def not_found(request):
    request.response.status = 404
    return {}


#@view_config(context=Exception, renderer = 'templates/internal_server_error.pt')
#def internal_server_error(request):
#    return {}


def build_error_latlong(latitude, longitude):
    return 'location not accepted latitude={0} longitude={1}'.format(latitude, longitude)


@view_config(route_name='transport:next:static', renderer='templates/transport_next_static.pt')
def transport_next_static(request):
    fname = sys._getframe().f_code.co_name
    alt_departure_type = 'Transportmiddel for avreise'
    from_dt = '2015-01-01T00:00:00Z'
    from_time = '00:00'
    latitude = u'59.892501'
    limit, error = _parse_limit_or_error(request)
    longitude = u'10.619216'
    stop_name = 'Fornebu Vest'
    transport = None
    updated = datetime.datetime.utcnow()
    updated = TimeUtils().shift_to_timezone(updated, TIME_ZONE)
    updated_txt = updated.strftime('%H:%M')
    updated_label = 'Sist oppdatert kl '

    if 'latitude' in request.GET and 'longitude' in request.GET:
        latitude = request.GET['latitude']
        longitude = request.GET['longitude']

    try:
        logger.info('%s latitude=%s longitude=%s', fname, latitude, longitude)
        transport = public_transport_source.lookup_transport_for_stop(latitude, longitude, limit=limit)
    except RuterException as e:
        error = str(e)
        logger.error(str(e))
    return {'from':from_dt, 'from_time':from_time, 'alt_departure_type': alt_departure_type,
            'updated_label': updated_label, 'updated_txt':updated_txt, 'stop_name':stop_name,
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
    fname = sys._getframe().f_code.co_name
    try:
        if 'latitude' in request.GET and 'longitude' in request.GET:
            latitude = request.GET['latitude']
            longitude = request.GET['longitude']
            limit, error = _parse_limit_or_error(request)
            if not input_validation.is_valid_wgs_84(latitude, longitude):
                logger.info('%s invalid parameter', fname)
                request.response.status = 400
                return {'error': build_error_latlong(latitude, longitude), 'params': ['latitude', 'longitude']}
            else:
                if type(limit) == int:
                    logger.info('%s latitude=%s longitude=%s limit=%s', fname, latitude, longitude, limit)
                    transport = public_transport_source.lookup_transport_for_stop(latitude, longitude, limit=limit)
                else:
                    logger.info('%s latitude=%s longitude=%s',fname, latitude, longitude)
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
    fname = sys._getframe().f_code.co_name
    dt_separator = 'til'
    error = None
    postnummer = '1364'
    temperature = '0'

    if 'postnummer' in request.GET:
        postnummer = request.GET['postnummer']
        logger.info('%s postnummer=%s',fname, postnummer)
        if not input_validation.is_valid_postnummer(postnummer):
            request.response.status = 400
            return {'error': 'postnummer not accepted', 'params': ['postnummer']}

    try:
        first_forecast = lookup_forecast_for_postnummer(postnummer)
        bind_headers_for_forecast(request, first_forecast)
        weather_h1 = first_forecast.place.name
        forecast = [first_forecast]
    except YrException as e:
        error = str(e)
        logger.error(str(e))
    else:
        logger.info('%s',fname)

    return {'temperature': temperature, 'dt_separator': dt_separator, 'forecast':forecast, 'weather_h1': weather_h1,
            'error': error}


def _lookup_forecasts_for_lat_long(latitude, longitude):
    fname = sys._getframe().f_code.co_name
    logger.debug('%s', fname)
    zip_places = lookup_postnummer_closest_to(latitude, longitude)
    forecast = []
    for zp in zip_places:
        logger.debug('Lookup forecast for %s', zp.zip)
        f = lookup_forecast_for_postnummer(zp.zip)
        forecast.append(f)
    for f in forecast:
        try:
            logger.debug('Returning forecast for %s', f.place.name)
        except:
            pass
    return forecast


def bind_headers_for_forecast(request, forecast):
    logger.debug('Building headers ETag and Expires')
    last_date = forecast.time_forecasts[-1].to
    last_date_dt = dateutil.parser.parse(last_date)
    zip = forecast.place.zip
    expires = http_date(last_date_dt)
    logger.debug('Expires %s', expires)
    request.response.expires = expires
    etag = 'forecast;{};{}'.format(zip, last_date_dt)
    request.response.etag = etag
    logger.debug('ETag %s', etag)


@view_config(route_name='forecast', renderer='json')
def forecast(request):
    fname = sys._getframe().f_code.co_name
    try:
        if 'postnummer' in request.GET:
            postnummer = request.GET['postnummer']
            logger.info('%s postnummer=%s',fname, postnummer)
            if not input_validation.is_valid_postnummer(postnummer):
                request.response.status = 400
                return {'error': 'postnummer not accepted', 'params': ['postnummer']}
            else:
                first_forecast = lookup_forecast_for_postnummer(postnummer)
                bind_headers_for_forecast(request, first_forecast)
                return {'error': None, 'forecast': [first_forecast]}
        elif 'latitude' in request.GET and 'longitude' in request.GET:
            latitude = request.GET['latitude']
            longitude = request.GET['longitude']
            logger.info('%s latitude=%s longitude=%s',fname, latitude, longitude)
            if not input_validation.is_valid_wgs_84(latitude, longitude):
                request.response.status = 400
                return {'error': build_error_latlong(latitude, longitude), 'params': ['latitude', 'longitude']}
            else:
                forecast_latlong = _lookup_forecasts_for_lat_long(latitude, longitude)
                first_forecast = forecast_latlong[0]
                bind_headers_for_forecast(request, first_forecast)

                return {'error': None, 'forecast': forecast_latlong}
        elif len(request.params) > 0:
            logger.info('%s invalid parameters',fname)
            request.response.status = 400
            return {'error': 'Missing parameters', 'params': ['postnummer', 'latitude', 'longitude']}
        else:
            logger.info('%s',fname)
            return {'info': 'Pass parameters postnummer from posten or a pair of latitude, longitude. \
The response is the current weather forecast', 'params': ['postnummer', 'latitude', 'longitude']}
    except YrException as e:
        message = str(e)
        request.response.status = 500
        logger.error(message)
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
