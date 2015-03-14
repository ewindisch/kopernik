#!/usr/bin/env python3.4
from collections import namedtuple
import flask
from flask import request
import kopernik.backends.proxy.driver
import json
import uuid
import sys
import os
import urllib.parse

import kopernik.client
from kopernik.endpoint import app as kopernik_app


if __name__ == "__main__":
    # Where backend is an object graph database...
    # examples are built on top of property graphs and
    # sources not natively graphed.
    #backend = kopernik.contrib.sensors.etcd.etcdproxy.BackendEtcd()
    backend_url = os.environ.get('BACKEND_PORT', None)
    if not backend_url:
        raise Exception("No backend url specified as BACKEND_PORT in environment.")

    # Transform docker links URLs
    backend_url_parts = urllib.parse.urlparse(backend_url)
    if backend_url_parts[0] == 'tcp':
        backend_url_parts[0] = 'http'
        backend_url = urllib.parse.urnunparse(peer_url_parts)

    kopernik.endpoint.backend = kopernik.backends.proxy.driver.BackendProxy(backend_url)

    port = os.environ.get('KOPERNIK_PORT', 80)
    peer = os.environ.get('KOPERNIK_PEER', None)
    if peer:
        client = kopernik.client.KopernikClient(peer)
        client.register(kopernik_app.host_uuid)
        while True:
            sleep(1)
    kopernik_app.run(host='0.0.0.0', port=port, debug=True)
