'''
An example of building a Linux-based Koperik host
which provides sensors via i2c.
'''
import smbus
import time
import uuid

i2c_bus = smbus.SMBus(0)
i2c_address = 0x60


class BackendGenericI2C(object):
    def __init__(self, machine_id):
        self._machine_id = machine_id

        # Create a node per i2c register
        self._nodes = { uuid.uuid5(self._machine_id, x): x
                        for x in range(1, 255) }

    def nodes(self, limit=5):
        return iter(self._nodes)

    def node(self, node_id):
        return bus.read_byte_data(i2c_address, self._nodes[node_id])

    def create(self, nodeURN, properties):
        '''
        This driver is static and cannot create new nodes.
        '''
        return False

    def delete(self, node_id):
        '''
        This driver is static and cannot create new nodes.
        '''
        return False
