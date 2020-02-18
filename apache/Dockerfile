FROM httpd:2.4

COPY httpd.conf /usr/local/apache2/conf/httpd.conf
COPY apache-start.sh ./apache-start.sh
COPY loganfordnet /home/loganfordnet

RUN useradd -ms /bin/bash loganfordnet
RUN useradd -ms /bin/bash apache

RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
    default-mysql-server \
    python3-pip \
    gcc

RUN pip3 install wheel && \
    pip3 install setuptools && \
    pip3 install mod-wsgi &&\
    pip3 install PyMySQL && \
    pip3 install alembic==1.0.10 && \
    pip3 install pyramid_chameleon && \
    pip3 install -e /home/loganfordnet