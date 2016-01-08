# -*- coding: utf-8 -*-
import datetime
import sys
import input_validation
from .weather import Time
from .weather_source import lookup_forecast_for_postnummer
from .webutils import http_date
from pyramid.view import view_config, notfound_view_config
import logging
from time_utils import TimeUtils

logger = logging.getLogger(__name__)


def _filter_forecast_fields(forecasts, request_keys):
    responses = [None] * len(forecasts)
    for i, forecast in enumerate(forecasts):
        request_keys = request_keys.split(',')
        f = forecast.__json__(None).keys()
        response_keys = set(request_keys) & set(f)
        response = {}
        for rk in response_keys:
            response[rk] = f[rk]
        responses[i] = response
    return responses


def _filter_forecast_date(forecasts, date):
    today = date.strftime('%Y-%m-%d')
    return filter(lambda x: x.start.startswith(today), forecasts)


@view_config(route_name='forecast:now', renderer='json')
def forecast_now(request):
    fname = sys._getframe().f_code.co_name
    forecast_response = None
    error = None
    if 'postnummer' in request.GET:
        postnummer = request.GET['postnummer']
        logger.info('%s postnummer=%s',fname, postnummer)
        if input_validation.is_valid_postnummer(postnummer):
            full_forecast = lookup_forecast_for_postnummer(postnummer)
            forecast = full_forecast.time_forecasts
            today = datetime.datetime.now()
            forecast = _filter_forecast_date(forecast, today)
            if 'keys' in request.GET:
                request_keys = request.GET['keys']
                forecast_response = _filter_forecast_fields(forecast, request_keys)
            else:
                forecast_response = forecast
            day = datetime.datetime.now()
            date = day.strftime('%Y-%m-%d')
            request.response.etag = '{};{};{}'.format(fname, postnummer, date)

            last_date = day + datetime.timedelta(days=1)
            request.response.expires = http_date(last_date)
        else:
            request.response.status = 400
            error = 'Invalid postnummer'
    else:
        logger.info('%s', fname)
        request.response.status = 422
        error = 'Provide parameter postnummer'
    return {'error':error, 'forecast':forecast_response}


@view_config(route_name='forecast:now:keys', renderer='json')
def forecast_keys(request):
    fname = sys._getframe().f_code.co_name
    logger.info('%s', fname)
    error = None
    keys = Time().__json__(None).keys()
    return {'error':error, 'keys':keys}


@view_config(route_name='datetime:now', renderer='json')
def datetime_now(request):
    fname = sys._getframe().f_code.co_name
    logger.info('%s', fname)
    dt = TimeUtils().timenow_system_with_timezone()
    time_s = dt.isoformat()
    request.response.headers['Cache-Control'] = 'no-cache'
    request.response.expires = http_date(dt)
    return {'time':time_s}