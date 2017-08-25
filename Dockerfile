FROM python:3.6-alpine
MAINTAINER Aloys Augustin <aloys@scalr.com>

RUN apk add --no-cache build-base linux-headers pcre-dev && \
    pip3 install uwsgi

ADD . /opt/example-hostname-webhook

RUN pip3 install -r /opt/example-hostname-webhook/requirements.txt

CMD ["uwsgi", "--ini", "/opt/example-hostname-webhook/uwsgi.ini"]

