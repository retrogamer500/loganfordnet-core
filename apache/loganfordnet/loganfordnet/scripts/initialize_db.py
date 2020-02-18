import argparse
import sys
import os

from pyramid.paster import bootstrap, setup_logging, get_appsettings
from sqlalchemy.exc import OperationalError

from .. import models
from ..models.meta import Base
from ..models import get_engine


def expand_vars(settings):
    d = {}
    for key, value in settings.items():
        d[key]=os.path.expandvars(value)
    return d


def setup_models(dbsession, settings):
    """
    Add or update models / fixtures in the database.

    """
    
    rootUser = models.User(name='root', role='admin')
    rootUser.set_password(settings['root.password'])
    dbsession.add(rootUser)
    
    permission = models.Permission(name='admin.user', group='admin', description='Access user administration')
    dbsession.add(permission)
    permission2 = models.Permission(name='csgo.10man.submit', group='csgo', description='Submit CSGO matches on 10-man page')
    dbsession.add(permission2)
    permission3 = models.Permission(name='pages.admin', group='pages', description='Create and edit pages')
    dbsession.add(permission3)
    
    user_permission = models.UserPermission(name='admin.user', user=rootUser, setting=1)
    dbsession.add(user_permission)


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'config_uri',
        help='Configuration file, e.g., configuration.ini',
    )
    return parser.parse_args(argv[1:])


def main(argv=sys.argv):
    args = parse_args(argv)
    setup_logging(args.config_uri)
    env = bootstrap(args.config_uri)

    try:
        with env['request'].tm:
            dbsession = env['request'].dbsession
            settings = expand_vars(get_appsettings(args.config_uri))
            engine = get_engine(settings)
            Base.metadata.create_all(engine)
            
            setup_models(dbsession, settings)
    except OperationalError:
        print('''
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to initialize your database tables with `alembic`.
    Check your README.txt for description and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.
            ''')
