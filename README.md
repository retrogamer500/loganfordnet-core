# loganfordnet-core

## Setup

The steps below assume that, if you are running Windows, that you have installed Git Bash, Mingw, or some other way of executing linux commands under Windows. The working directory should also be the loganfordnet-core folder.

1. Copy over environments file. You will have to populate some data marked with `POPULATE ME PLEASE! AND DON'T COMMIT TO VERSION CONTROL`.

    `cp ./config/develop/config.env ./config.env`

2. Install Docker

    `sudo apt-get install docker.io`

3. Install Docker-Compose

    `sudo apt-get install docker-compose`

4. Edit hosts file

    You may want to edit your hosts file (In Windows it is located in C:\Windows\System32\Drivers\etc\hosts). That way when you visit loganford.net, you will access the site running on your local machine. When you do this, make sure you type loganford.net into your browser, without any www or trailing slash. If you don't do this, then subdomains may not work correctly.

    ```
    127.0.0.1    loganford.net
    127.0.0.1    jellyfin.loganford.net
    127.0.0.1    ombi.loganford.net
    127.0.0.1    jackett.loganford.net
    127.0.0.1    sonarr.loganford.net
    127.0.0.1    radarr.loganford.net
    127.0.0.1    transmission.loganford.net
    127.0.0.1    teamspeak.loganford.net
    ```

## Running site

Just execute the following bash script: `./run.sh`

Command line options:

* `-b`: rebuild docker containers

## Removing old docker images/volumes

Docker caches some steps, so if you want to test the full build process, you can run these commands to removed cached images and volumes. The mysql database also is stored outside of docker to ensure that on a restart, the data is not destroyed. Running these commands will restore the database to a fresh start.

```
docker-compose down
docker rmi $(docker images -a -q)
docker system prune --volumes
```

## Updating database

Todo: add documentation here

## Setting up media serving

Todo: add documentation here

## Todo list
* ~~Add auth ticket tokens on login, verify in httpd~~
* ~~Add user configurations for subdomain access, and add links in sidebar~~
* ~~Add teamspeak @loganford.net~~
* Update dev and prod env files
* Refactor view project structure to keep templates in the same folder as views
* Clean up scripts and sql folder, and remove unneeded scripts
* Add SSL support
* Move teamspeak over to teamspeak.loganford.net?
* LDAP support + authorization in pyramid