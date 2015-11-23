from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('index', '/index')
    config.add_route('index:authenticate', '/index/authenticate')
    config.add_route('index:static', '/index/static')
    config.add_route('transport:next', '/transport/next')
    config.add_route('forecast', '/forecast')
    config.add_route('mail:calendar', '/mail/calendar')

    config.scan()
    return config.make_wsgi_app()
