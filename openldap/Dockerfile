FROM osixia/openldap:1.3.0

ARG BUILD_ENV
ENV BUILD_ENV=${BUILD_ENV:-"prod"}

ENV PREFIX=/opt
ENV OPENLDAP_INSTALL_DIR=${PREFIX}/ldap
ENV OPENLDAP_VERSION=2.4.48

# Temporary install deps
RUN apt-get update
RUN apt-get install -y wget build-essential git libtool libdb-dev groff groff-base

# Build tmp OpenLDAP
RUN mkdir -p ${PREFIX}
WORKDIR ${PREFIX}
RUN wget ftp://ftp.openldap.org/pub/OpenLDAP/openldap-release/openldap-${OPENLDAP_VERSION}.tgz
RUN tar xzf openldap-${OPENLDAP_VERSION}.tgz
RUN mv openldap-${OPENLDAP_VERSION} ldap
WORKDIR ${OPENLDAP_INSTALL_DIR}
RUN ./configure --prefix=${PREFIX} --enable-modules
RUN make depend
RUN make
RUN make install

# Build bcrypt OpenLDAP
RUN mkdir -p ${OPENLDAP_INSTALL_DIR}/contrib/slapd-modules/passwd
WORKDIR ${OPENLDAP_INSTALL_DIR}/contrib/slapd-modules/passwd
RUN git clone https://github.com/wclarie/openldap-bcrypt.git bcrypt
WORKDIR ${OPENLDAP_INSTALL_DIR}/contrib/slapd-modules/passwd/bcrypt
RUN make
RUN make install

# install BCrypt lib
RUN cp /usr/local/libexec/openldap/pw-bcrypt.so /usr/lib/ldap/pw-bcrypt.so

# Remove tmp OpenLDAP build
RUN rm -rf ${OPENLDAP_INSTALL_DIR}
RUN rm -rf /usr/local/libexec

# Remove installed deps
RUN apt-get remove -y wget build-essential git libtool libdb-dev groff groff-base
RUN apt-get autoclean && \
  rm -rf /var/lib/apt/lists/* && \
  rm -rf /usr/share/locale/* && \
  rm -rf /usr/share/man/* && \
  rm -rf /usr/share/doc/*

# Osixia/OpenLDAP extension
COPY enable-bcrypt.ldif /container/service/slapd/assets/config/bootstrap/ldif/custom/enable-bcrypt.ldif
COPY create-ou.ldif /container/service/slapd/assets/config/bootstrap/ldif/custom/create-ou.ldif

WORKDIR /