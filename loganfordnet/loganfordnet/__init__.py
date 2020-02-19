import os

from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """    
    settings = expand_vars(settings)
    
    with Configurator(settings=settings) as config:
        config.include('.models')
        config.include('pyramid_chameleon')
        config.include('.routes')
        config.include('.security')
        my_session_factory = SignedCookieSessionFactory(settings['auth.secret'])
        config.set_session_factory(my_session_factory)
        config.scan()
    return config.make_wsgi_app()


def expand_vars(settings):
    d = {}
    for key, value in settings.items():
        d[key]=os.path.expandvars(value)
    return d
