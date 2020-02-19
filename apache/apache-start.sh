#!/bin/bash

#This script is run on startup

#Wait for mysql
while ! mysqladmin ping -h"mysql" --silent; do
    echo "Waiting for mysql"
    sleep 1
done

echo "Mysql has started"

#Initialize DB
userTableOutput=$(mysql -h mysql -u root -p$MYSQL_ROOT_PASSWORD loganfordnet -e "show tables like \"user\"")
if [ -z "$userTableOutput" ]
then
    echo "Database not set up for loganfordnet"
    pushd /home/loganfordnet/
    find /home/loganfordnet/ -name "*.pyc" -exec rm -f {} \;
    /usr/bin/python3.7 -m loganfordnet.scripts.initialize_db /home/loganfordnet/configuration.ini
    popd
    echo "Done initializing database"
else
    echo "Existing loganfordnet database found"
fi

#Todo: perform SQL updates?

#Run gunicorn
pushd /home/loganfordnet/
find /home/loganfordnet/ -name "*.pyc" -exec rm -f {} \;
gunicorn3 -b 0.0.0.0:8000 --workers=5 wsgi:app &
popd

#Run apache
apachectl -D FOREGROUND

#Don't think I need this
#tail -f /dev/null