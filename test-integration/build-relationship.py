#!/usr/bin/env python3.4
import kopernik.client
import kopernik.model
import os

'''
Builds a relationship and tests it.
This is an example of how terrible the API is.
Improving these integration tests will improve usability
of the API itself (I hope!)
'''

host = os.environ.get('KOPERNIK_HOST', None)
client = kopernik.client.KopernikClient(host)

node1 = client.create('urn:kopernik:object', name="bob")
node2 = client.create('urn:kopernik:object', name="alice")

link_node = client.create('urn:kopernik:relationship',
                          node1_URN_str=node1,
                          node2_URN_str=node2)
lnode_data = client.node(link_node)
node2_urn = lnode_data['node2_URN_str']

if node2 != node2_urn:
    print("ERROR: node2 and node2_urn don't match")

node2_data = client.node(node2_urn)

if node2_data['name'] != "alice":
    print("ERROR: node2 name should be alice")

