class CrudBackend(object):
    def __init__(self):
        pass

    def create(self, key, data=None):
        return NotImplementedError()

    def read(self, key):
        return NotImplementedError()

    def update(self, key, data):
        return NotImplementedError()

    def delete(self, key):
        return NotImplementedError()

    def has_node(self, key):
        return NotImplementedError()
