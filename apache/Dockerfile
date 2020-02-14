FROM httpd:2.4

RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
    libapache2-mod-wsgi-py3

COPY httpd.conf /usr/local/apache2/conf/httpd.conf

RUN useradd -ms /bin/bash pyramid

COPY pyramid /home/pyramid