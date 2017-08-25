FROM debian:jessie-slim
MAINTAINER Aloys Augustin <aloys@scalr.com>

RUN apt-get update && \
    apt-get install python python-dev python-pip uwsgi uwsgi-plugin-python

ADD . /opt/example-hostname-webhook

RUN pip install -r /opt/example-hostname-webhook/requirements.txt

CMD ["/usr/local/bin/uwsgi", "--ini", "/opt/example-hostname-webhook/uwsgi.ini"]

