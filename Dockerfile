#++++++++++++++++++++++++++++++++++++++#
#   Coder Ideas container in Alpine    #
#++++++++++++++++++++++++++++++++++++++#

FROM python:3.8.2-alpine3.11
LABEL vendor=Featx
MAINTAINER Excepts <excepts@featx.org>

ARG CODER_HOME=/usr/local/coder
ARG CODER_VERSION=1.0.0
ARG GROUP=featx
ARG USER=featx

COPY . $CODER_HOME/

RUN set -ex && mkdir -p $CODER_HOME &&\
    addgroup -g 1000 $GROUP && adduser -G $GROUP -u 1000 -s /sbin/nologin -D -H $USER &&\
    apk add --no-cache --virtual .build-deps build-base libffi-dev openssl-dev &&\
    cd $CODER_HOME &&\
    pip install -r requirements.txt &&\
    apk del .build-deps &&\
    rm -rf /var/cache/apk/* &&\
    apk add -U git &&\
    chown -R $GROUP:$USER $CODER_HOME

EXPOSE 8080
VOLUME ["/usr/local/coder/config"]
WORKDIR $CODER_HOME
USER $USER
#ENTRYPOINT ["entry"]
CMD ["python", "main.py"]
