FROM debian:jessie-slim
MAINTAINER Aloys Augustin <aloys@scalr.com>

RUN apt-get update && \
    apt-get install -y --no-install-recommends python python-dev python-pip uwsgi uwsgi-plugin-python && \
    groupadd uwsgi && \
    useradd -g uwsgi uwsgi

ADD . /opt/example-hostname-webhook

RUN pip install -r /opt/example-hostname-webhook/requirements.txt

CMD ["/usr/bin/uwsgi", "--ini", "/opt/example-hostname-webhook/uwsgi.ini"]

