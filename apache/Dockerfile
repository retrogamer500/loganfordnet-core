FROM httpd:2.4

COPY httpd.conf /usr/local/apache2/conf/httpd.conf
RUN useradd -ms /bin/bash apache

RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
    git \
    ca-certificates \
    build-essential \
    apache2-dev && \
    git clone https://github.com/gavincarr/mod_auth_tkt.git && \
    cd mod_auth_tkt && \
    ./configure --apxs=/usr/local/apache2/bin/apxs && \
    make && \
    make install && \
    cd ..