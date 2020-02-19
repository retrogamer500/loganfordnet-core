"""Pyramid bootstrap environment. """
import os

from alembic import context
from pyramid.paster import get_appsettings, setup_logging
from sqlalchemy import engine_from_config

from loganfordnet.models.meta import Base

import sys
sys.path.insert(0, '/home/logan/loganfordnet/loganfordnet/')

config = context.config

setup_logging(config.config_file_name)

settings = get_appsettings(config.config_file_name)
target_metadata = Base.metadata


def expand_vars(settings):
    d = {}
    for key, value in settings.items():
        d[key]=os.path.expandvars(value)
    return d


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(url=expand_vars(settings)['sqlalchemy.url'])
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    engine = engine_from_config(expand_vars(settings), prefix='sqlalchemy.')

    connection = engine.connect()
    context.configure(
        connection=connection,
        target_metadata=target_metadata
    )

    try:
        with context.begin_transaction():
            context.run_migrations()
    finally:
        connection.close()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
