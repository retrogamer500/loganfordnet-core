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
    initialize_loganfordnet_db ./loganfordnet/configuration.ini
else
    echo "Existing loganfordnet database found"
fi

#Todo: perform SQL updates?

#Run apache
apachectl -D FOREGROUND

#Don't think I need this
#tail -f /dev/null