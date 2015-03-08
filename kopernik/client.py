#!/usr/bin/env python
import json
import requests


class KopernikClient(object):
    def __init__(self, base_uri):
        self.base_uri = base_uri or 'http://localhost/'

    def nodes(self):
        return requests.get(self.base_uri + 'nodes').json()

    def node(self, nodeid):
        print("Requesting node: {}".format(nodeid))
        result = requests.get(self.base_uri + 'node/{}'.format(nodeid))
        if result.status_code == 200:
            return result.json()
        else:
            return result.status_code

    def create(self, class_URN_str, **kwargs):
        headers = {'content-type': 'application/json'}
        args = dict({
            'class_URN_str': class_URN_str
        }, **kwargs)
        return requests.post(self.base_uri + 'node', data=json.dumps(args), headers=headers).json()

    def delete(self, nodeid):
        print("Requesting node: {}".format(nodeid))
        answer = requests.delete(self.base_uri + 'node/{}'.format(nodeid))
        return (answer.status_code, answer.reason, answer.text)

if __name__ == "__main__":
    client = KopernikClient('http://localhost/')
    nodeid = client.create('bob', dog='hello')
    print(client.nodes())
    print(client.node(nodeid))
    print(client.delete(nodeid))
    print(client.node(nodeid))
