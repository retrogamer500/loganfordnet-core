#!/bin/bash
source include.sh

if [ $LF_ENVIRONMENT = "dev" ]; then
    cd "$(dirname "$0")"
    cd ..
    echo "Working directory: `pwd`"
    export VENV=$HOME/loganfordnetvenv

    #delete existing DB if exists
    #mysql_upgrade -u root -pjumpthrow
    #systemctl restart mysqld
    mysql -u user -p$LF_MYSQL_PASS -e "drop database loganfordnet;"
    mysql -u user -p$LF_MYSQL_PASS -e "create database loganfordnet;"

    #rebuild DB
    $VENV/bin/initialize_loganfordnet_db development.ini
    #$VENV/bin/alembic -c development.ini revision --autogenerate
    #$VENV/bin/alembic -c development.ini upgrade head

    #start server
    $VENV/bin/pserve development.ini --reload
fi
