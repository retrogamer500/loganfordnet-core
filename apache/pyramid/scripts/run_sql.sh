#!/bin/bash
source include.sh

echo "Running upgrade SQL..."
sudo mysql -u root -p$LF_MYSQL_ROOT_PASS loganfordnet < ../sql/upgrade.sql

echo "Running custom SQL..."
sudo mysql -u root -p$LF_MYSQL_ROOT_PASS loganfordnet < ../sql/custom.sql

echo "Creating folder to put used sql"
newfolder=../sql/released/$(date "+%F-%T")
mkdir $newfolder

echo "Moving sql to released folder"
mv ../sql/upgrade.sql $newfolder
mv ../sql/custom.sql $newfolder
