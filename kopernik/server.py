import wsgiref

class KopernikWsgiServer(object):
    def __init__(self):
        pass

ws = KopernikWsgiServer(protocols=['restjson'])
app = ws.wsgiapp()

