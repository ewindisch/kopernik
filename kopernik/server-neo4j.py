from collections import namedtuple
import flask
from flask import request
#import kopernik.contrib.sensors.etcd.etcdproxy
import kopernik.backends.neo.driver
import json
import uuid
import sys
import os
import urllib.parse

import kopernik.client

app = flask.Flask(__name__)
from kopernik.endpoint import app as kopernik_app


if __name__ == "__main__":
    # Where backend is an object graph database...
    # examples are built on top of property graphs and
    # sources not natively graphed.
    #backend = kopernik.contrib.sensors.etcd.etcdproxy.BackendEtcd()
    db_url = os.environ.get('NEO4J_PORT', 'http://localhost:7474/db/data/')

    # Transform docker links URLs
    db_url_parts = urllib.parse.urlparse(db_url)
    if db_url_parts[0] == 'tcp':
        db_url_parts[0] = 'http'
        db_url = urllib.parse.urnunparse(db_url_parts)

    kopernik.endpoint.backend = kopernik.backends.neo.driver.BackendNeo4j(db_url)

    port = os.environ.get('KOPERNIK_PORT', 80)
    peer = os.environ.get('KOPERNIK_PEER', None)
    if peer:
        client = kopernik.client.KopernikClient(peer)
        client.register(kopernik_app.host_uuid)
        while True:
            sleep(1)
    kopernik_app.run(host='0.0.0.0', port=port, debug=True)
