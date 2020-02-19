#!/bin/bash
source include.sh

if [ $LF_ENVIRONMENT = "dev" ]; then
    cd ..
    source $HOME/loganfordnetvenv/bin/activate
    rm loganfordnet/alembic/versions/*.py
    alembic -c development.ini revision --autogenerate
    alembic -c development.ini upgrade head --sql | tail -n+8 | head -n -3 > sql/upgrade.sql
else
    cd ..
    rm loganfordnet/alembic/versions/*.py
    alembic -c production.ini revision --autogenerate
    alembic -c production.ini upgrade head --sql | tail -n+8 > sql/upgrade.sql
fi
