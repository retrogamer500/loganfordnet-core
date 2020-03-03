FROM ubuntu:xenial-20200114

COPY startup.sh ./startup.sh

RUN useradd -ms /bin/bash loganfordnet

RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
    mysql-client \
    python3-pip \
    gunicorn3 \
    gcc \
    python3-dev \
    build-essential \
    libffi-dev \
    libldap2-dev \ 
    libsasl2-dev

RUN pip3 install wheel && \
    pip3 install setuptools && \
    pip3 install PyMySQL && \
    pip3 install alembic==1.0.10 && \
    pip3 install pyramid_chameleon