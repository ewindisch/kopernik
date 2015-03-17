#!/usr/bin/env python
import json
import requests
import urllib.parse

import kopernik.model


class KopernikClient(object):
    def __init__(self, base_uri):
        self.base_uri = base_uri or 'http://localhost/'

    def _request(self, method, uri, **kwargs):
        url = urllib.parse.urljoin(self.base_uri, uri)
        return getattr(requests, method)(url, **kwargs)

    def nodes(self):
        return self._request('get', 'nodes').json()

    def node(self, nodeid):
        print("Requesting node: {}".format(nodeid))
        result = self._request('get', 'node/{}'.format(nodeid))
        if result.status_code == 200:
            return result.json()
        else:
            return result.status_code

    def create(self, class_URN_str, **kwargs):
        headers = {'content-type': 'application/json'}
        args = dict({
            'class_URN_str': class_URN_str
        }, **kwargs)
        post = self._request('post', 'node', data=json.dumps(args), headers=headers)
        return post.json()

    def delete(self, nodeid):
        print("Requesting node: {}".format(nodeid))
        answer = self._request('delete', 'node/{}'.format(nodeid))
        return (answer.status_code, answer.reason, answer.text)

    def register(self, nodeid):
        """Register a peer. This simply creates a node of the KopernikNode class."""
        client.create('KopernikNode', nodeid=nodeid)
