#!/usr/bin/env python

from flask import Flask
from flask import request
from flask import abort

import pytz
import string
import random
import json
import logging
import binascii
import dateutil.parser
import hmac

from hashlib import sha1
from datetime import datetime



config_file = './config_prod.json'

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)

# will be overridden if present in config_file
SCALR_SIGNING_KEY = ''


@app.route("/hostname/", methods=['POST'])
def webhook_listener():
    if not validate_request(request):
        abort(403)

    data = json.loads(request.data)
    if 'eventName' not in data or 'data' not in data:
        logging.info('Invalid request received')
        abort(404)

    if data['eventName'] == 'HostnameRequest':
        return compute_hostname(data['data'])
    else:
        logging.info('Received request for unhandled event %s', data['eventName'])
        return ''


def compute_hostname(data):
    # Add custom logic here to generate the hostname of your servers.
    # All the global variables that are defined on the server are available in the "data" dict.
    # You can make API calls to Scalr to get additional details about this server, or query any other system.
    # It is your responsibility to ensure that you do not assign the same hostname to two servers, 
    # Scalr will not enforce unicity.

    # As an example we just generate a random string with 10 letters and 3 numbers
    hostname = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
    hostname += ''.join(random.choice(string.digits) for i in range(3))
    return hostname.lower()


def validate_request(request):
    if 'X-Signature' not in request.headers or 'Date' not in request.headers:
        return False
    date = request.headers['Date']
    body = request.data
    expected_signature = binascii.hexlify(hmac.new(SCALR_SIGNING_KEY, body + date, sha1).digest())
    if expected_signature != request.headers['X-Signature']:
        return False
    date = dateutil.parser.parse(date)
    now = datetime.now(pytz.utc)
    delta = abs((now - date).total_seconds())
    return delta < 300


def load_config(filename):
    with open(filename) as f:
        options = json.loads(f.read())
        for key in options:
            if key in []:
                logging.info('Loaded config: {}'.format(key))
                globals()[key] = options[key]
            elif key in ['SCALR_SIGNING_KEY']:
                logging.info('Loaded config: {}'.format(key))
                globals()[key] = options[key].encode('ascii')


load_config(config_file)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
