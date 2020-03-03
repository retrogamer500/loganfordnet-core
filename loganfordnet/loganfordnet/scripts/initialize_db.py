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
    rootUser.create_ldap_user(settings['root.password'], settings)
    dbsession.add(rootUser)
    
    dbsession.add(models.Permission(name='admin_user', group='admin', description='Access user administration'))
    dbsession.add(models.Permission(name='pages_admin', group='pages', description='Create and edit pages'))
    dbsession.add(models.Permission(name='subdomain_jellyfin', group='subdomain', description='Access Jellyfin'))
    dbsession.add(models.Permission(name='subdomain_ombi', group='subdomain', description='Access Ombi'))
    dbsession.add(models.Permission(name='subdomain_jackett', group='subdomain', description='Access Jackett'))
    dbsession.add(models.Permission(name='subdomain_sonarr', group='subdomain', description='Access Sonarr'))
    dbsession.add(models.Permission(name='subdomain_radarr', group='subdomain', description='Access Radarr'))
    dbsession.add(models.Permission(name='subdomain_transmission', group='subdomain', description='Access Transmission'))
    
    user_permission = models.UserPermission(name='admin_user', user=rootUser, setting=1)
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

if __name__ == "__main__":
    main(sys.argv)