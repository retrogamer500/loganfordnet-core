#!/bin/bash

#This script is run on startup

#Wait for mysql
while ! mysqladmin ping -h"mysql" --silent; do
    echo "Waiting for mysql"
    sleep 1
done

echo "Mysql has started"

#Install project
if [ ! -f /var/setup_finished ]; then
    pip3 install -e /home/loganfordnet
    touch /var/setup_finished
fi

#Initialize DB
userTableOutput=$(mysql -h mysql -u root -p$MYSQL_ROOT_PASSWORD loganfordnet -e "show tables like \"user\"")
if [ -z "$userTableOutput" ]
then
    echo "Database not set up for loganfordnet"
    pushd /home/loganfordnet/
    find /home/loganfordnet/ -name "*.pyc" -exec rm -f {} \; #Fix weird magic number issues
    python3 -m loganfordnet.scripts.initialize_db /home/loganfordnet/configuration.ini
    popd
    echo "Done initializing database"
else
    echo "Existing loganfordnet database found"
fi

#Run gunicorn
GUNICORN_ARGS=""
if [ "$ENVIRONMENT" = "dev" ]; then
    GUNICORN_ARGS="${GUNICORN_ARGS} --reload"
fi

pushd /home/loganfordnet/
find /home/loganfordnet/ -name "*.pyc" -exec rm -f {} \; #Fix weird magic number issues
gunicorn3 -b 0.0.0.0:8000 --workers=5 wsgi:app ${GUNICORN_ARGS}