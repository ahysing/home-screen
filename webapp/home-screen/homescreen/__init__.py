from pyramid.config import Configurator
import logging
from .tracked_request import TrackedRequest

logger = logging.getLogger(__name__)


def application_locale_negotiator(request):
    if not hasattr(request, '_LOCALE_'):
        request._LOCALE_ = request.accept_language.best_match(
            ('no'), 'no')
    return request._LOCALE_


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings, locale_negotiator=application_locale_negotiator)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('index', '/')
    config.add_route('index:authenticate', '/index/authenticate')
    config.add_route('index:static', '/index/static')
    config.add_route('transport:next', '/transport/next')
    config.add_route('transport:next:static', '/transport/next/static')
    config.add_route('forecast', '/forecast')
    config.add_route('forecast:static', '/forecast/static')
    config.add_route('mail:calendar', '/mail/calendar')

    config.add_route('datetime:now', '/datetime/now')
    config.add_route('forecast:now', '/forecast/now')
    config.add_route('forecast:now:keys', '/forecast/now/keys')

    config.set_request_factory(TrackedRequest)
    config._add_tween('homescreen.tweens.log_tracker.LogTracker')

    config.scan()
    app = config.make_wsgi_app()
    logger.debug('Returning WGSI app' + str(app))
    return app

#__here__ = os.path.dirname(os.path.abspath(__file__))
