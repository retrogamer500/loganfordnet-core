FROM ubuntu:xenial-20200114

COPY startup.sh ./startup.sh
COPY . /home/loganfordnet

RUN useradd -ms /bin/bash loganfordnet

RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
    mysql-client \
    python3-pip \
    gunicorn3 \
    gcc \
    python3-dev \
    build-essential \
    libffi-dev 

RUN pip3 install wheel && \
    pip3 install setuptools && \
    pip3 install PyMySQL && \
    pip3 install alembic==1.0.10 && \
    pip3 install pyramid_chameleon && \
    pip3 install -e /home/loganfordnet