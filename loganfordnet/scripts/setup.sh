#!/bin/bash
source include.sh

echo "setup.sh running..."
cd "$(dirname "$0")"
cd ..
echo "Environment: $LF_ENVIRONMENT"
echo "Working directory: `pwd`"

#install SQLite 3
sudo apt-get install mysql-server -y

#install git
sudo apt-get install git -y

#install pip
sudo apt-get install python-pip -y

#setup python envoronment
if [ $LF_ENVIRONMENT = "dev" ]; then
    sudo apt-get install python3-venv -y
    export VENV=$HOME/loganfordnetvenv
    python3 -m venv $VENV
    $VENV/bin/pip install --upgrade pip setuptools
    $VENV/bin/pip install PyMySQL
    $VENV/bin/pip install tldextract
    $VENV/bin/pip install bleach
    $VENV/bin/pip install -e ".[testing]"
    $VENV/bin/pip install alembic==1.0.10
    
    $VENV/bin/easy_install pyramid_chameleon
else
    pip3 install --upgrade pip setuptools
    pip3 install PyMySQL
    pip3 install tldextract
    pip3 install bleach
    pip3 install -e .
    pip3 install alembic==1.0.10
    
    easy_install pyramid_chameleon
fi

#Mysql
echo "Use the following password for the installation wizzard: $LF_MYSQL_ROOT_PASS"
sudo mysql_secure_installation

sudo mysql -u root -p$LF_MYSQL_ROOT_PASS -e "GRANT ALL PRIVILEGES ON *.* TO 'user'@'localhost' IDENTIFIED BY '$LF_MYSQL_PASS';"
sudo mysql -u root -p$LF_MYSQL_ROOT_PASS -e "CREATE DATABASE loganfordnet;"

if [ $LF_ENVIRONMENT = "dev" ]; then
    $VENV/bin/initialize_loganfordnet_db development.ini
else
    initialize_loganfordnet_db production.ini
fi
