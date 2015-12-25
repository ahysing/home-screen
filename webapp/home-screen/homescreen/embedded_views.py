# -*- coding: utf-8 -*-
import datetime
import sys
import input_validation
from weather import Time
from weather_source import lookup_forecast_for_postnummer
from pyramid.view import view_config, notfound_view_config
import logging

logger = logging.getLogger(__name__)


def _filter_forecast_fields(forecast, request_keys):
    request_keys = request_keys.split(',')
    f = forecast.__json__(None).keys()
    response_keys = set(request_keys) & set(f)
    response = {}
    for rk in response_keys:
        response[rk] = f[rk]
    forecast = response
    return forecast


@view_config(route_name='forecast:now', renderer='json')
def forecast_now(request):
    fname = sys._getframe().f_code.co_name
    forecast = None
    error = None
    if 'postnummer' in request.GET:
        postnummer = request.GET['postnummer']
        logger.info('%s postnummer=%s',fname, postnummer)
        if input_validation.is_valid_postnummer(postnummer):
            full_forecast = lookup_forecast_for_postnummer(postnummer)
            forecast = full_forecast['time_forecasts'][0]
            if 'keys' in request.GET:
                request_keys = request.GET['keys']
                forecast = _filter_forecast_fields(forecast, request_keys)
        else:
            request.response.status = 400
            error = 'Invalid postnummer'
    else:
        logger.info('%s', fname)
        request.response.status = 422
        error = 'Provide parameter postnummer'
    return {'error':error, 'forecast':forecast}


@view_config(route_name='forecast:now:keys', renderer='json')
def forecast_keys(request):
    fname = sys._getframe().f_code.co_name
    logger.info('%s', fname)
    error = None
    keys = Time().__json__(None).keys()
    return {'error':error, 'keys':keys}


@view_config(route_name='time:now', renderer='json')
def time(request):
    fname = sys._getframe().f_code.co_name
    logger.info('%s', fname)
    time = datetime.datetime.now().isoformat()
    return {'time':time}