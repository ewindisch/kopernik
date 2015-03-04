#!/usr/bin/env python
import json
import requests


class KopernikClient(object):
    def nodes(self):
        return requests.get('http://localhost/nodes').json()

    def node(self, nodeid):
        print "Requesting node: %s" % (nodeid,)
        result = requests.get('http://localhost/node/%s' % (nodeid,))
        if result.status_code == 200:
            return result.json()
        else:
            return result.status_code

    def create(self, class_URN_str, **kwargs):
        headers = {'content-type': 'application/json'}
        args = dict({
            'class_URN_str': class_URN_str
        }, **kwargs)
        return requests.post('http://localhost/node', data=json.dumps(args), headers=headers).json()

    def delete(self, nodeid):
        print "Requesting node: %s" % (nodeid,)
        answer = requests.delete('http://localhost/node/%s' % (nodeid,))
        return (answer.status_code, answer.reason, answer.text)

if __name__ == "__main__":
    client = KopernikClient()
    nodeid = client.create('bob', dog='hello')
    print client.nodes()
    print client.node(nodeid)
    print client.delete(nodeid)
    print client.node(nodeid)
