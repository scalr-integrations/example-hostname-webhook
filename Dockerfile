FROM python:3.6-alpine
MAINTAINER Aloys Augustin <aloys@scalr.com>

RUN apk add --no-cache build-base linux-headers pcre-dev && pip3 install uwsgi

ADD . /opt/webhook

RUN pip3 install -r /opt/webhook/requirements.txt

CMD ["uwsgi", "--ini", "/opt/webhook/uwsgi.ini"]

