'''
This exists if only to keep the API sane.

Kopernik should be a database capable of supporting all
of the operations necessary to run a Kopernik backend
with minimal fuss!
'''
import requests


class BackendProxy(object):
    def __init__(self, host):
        self._remote_host = host

    def _request(self, method, uri, **kwargs):
        url = urlparse.parse.urljoin(self._remote_host, uri)
        return getattr(requests, method)(url, **kwargs)

    def nodes(self, limit=5):
        result = self._request('get', '/nodes')
        return iter(result.json())

    def node(self, node_id):
        result = self._request('get', '/node/{}'.format(node_id))
        return result.json()

    def create(self, nodeURN, properties):
        '''
        This is tricky because we cannot set the nodeURN
        on a created node in Kopernik.
        Perhaps we should be able to do this?
        '''
        raise NotImplementedError()

    def delete(self, node_id):
        result = self._request('delete', '/node/{}'.format(node_id))
        if result.status_code == 200:
            return True
        return False
