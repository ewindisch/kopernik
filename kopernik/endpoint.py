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

host_uuid = uuid.uuid4()

"""
Object Graph Database Model
---------------------------

Tenants:
- All nodes in the graph are an object.
- All relationships in the graph are a node with a base relationship class.
- All objects implement a class.
- Classes are represented by nodes.
- Every node, class, and relationship is identified by a universally global URN:uuid.
- URNs use UUID urn syntax.


"""

"""
All nodes are objects...
"""
ObjectStruct = namedtuple(
    "Object",
    (
        "URN_str",
        "name_str",
        "class_URN_str",
    )
)
ClassStruct = namedtuple(
    "Object",
    (
        "URN_str",
        "name_str",
        "class_URN_str",
    )
)


"""
All relationships are objects... and thus nodes
"""
RelationshipStruct = namedtuple(
    "Relationship",
    (
        "URN_str",
        "name_str",
        "class_URN_str", # type of relationship...

        "node1_URN_str",
        "node2_URN_str"
    )
)

"""
Global object Object...
"""
BaseObjectObject = ClassStruct(
    'urn:kopernik:object:::1',
    'object',
    # Is an object; self-referential...
    'urn:kopernik:object:::1'
)
#graph.register(BaseObjectObject)

"""
Global root node
"""
RootObject = ObjectStruct(
    "urn:kopernik:root:::1",
    "Graph Root",
    # Is an object
    "urn:kopernik:object:::1"
)
#graph.register(RootObject)

"""
Define the keyword relationships
"""
BaseRelationshipObject = ObjectStruct(
    'urn:kopernik:relationship:::1',
    'Relationship Object',
    # Is an object
    'urn:kopernik:object:::1',
)
#graph.register(BaseRelationshipObject)

BaseRelationship = RelationshipStruct(
    'urn:kopernik:relationship_to_root:::1',
    'RELATIONSHIP',
    # Is a Relationship
    'urn:kopernik:relationship:::1',

    # self -> ROOT
    'urn:kopernik:root:::1',
    'urn:kopernik:relationship:::1'
)
#graph.register(BaseRelationship)


def _register_with_peer(peer):
    """Registered with a peer"""
    #requests.post("http://parent/name", "")
    client = kopernik.client.KopernikClient(peer)
    client.create('KopernikNode')


@app.route("/nodes", methods=["GET"])
def get_nodes():
    #return flask.jsonify(list(backend.crud))
    nodes_iter = backend.nodes()
    nodes =  list(nodes_iter)
    #print "node list: %s" % (nodes,)
    return json.dumps(nodes)
    #return flask.jsonify(nodes)


@app.route("/node/<name>", methods=["GET"])
def node(name):
    #nodes = backend.nodes()
    #if name in nodes:
    #    return flask.jsonify(nodes[name])
    node = backend.node(name)
    if not node:
        flask.abort(404)
    return json.dumps(node)
    #return flask.jsonify(node)


@app.route("/node", methods=["POST"])
def create_node():
    properties = request.get_json(force=True)
    nodeURN = generate_urn()

    if not 'class_URN_str' in properties:
        # Exception - no class specified
        raise Exception("no class URN str in {s}".format(properties))
        flask.abort(400)

    #classNode = kopernik.get_node(properties['class_URN_str'])
    classNode = {}

    if classNode and not all([prop in properties for prop in classNode.properties]):
        # Interface not satisfied
        raise Exception("interface not satisfied")
        flask.abort(400)

    #try:
    backend.create(nodeURN, properties)
    #except Exception:
    #    flask.abort(500)
    return json.dumps(nodeURN)  #flask.jsonify(nodeURN)


@app.route("/node/<urn>", methods=["DELETE"])
def delete_node(urn):
    #try:
    result = backend.delete(urn)
    #except Exception, e:
    #    flask.abort(500)
    #return flask.jsonify(urn)
    return json.dumps(result)


@app.route("/node/<name>/property/<pname>", methods=["GET"])
def node_property(name, pname):
    node_properties = backend.node(name).properties
    return flask.jsonify(node_properties)
    flask.abort(404)


@app.route("/node/<name>/property/<pname>", methods=["UPDATE"])
def update_node_property(name, pname):
    try:
        #backend.create(name)
        pass
    except Exception:
        flask.abort(500)
    return flask.jsonify(name)


def generate_urn():
    return uuid.uuid5(host_uuid, str(uuid.uuid4())).urn

if __name__ == "__main__":
    global backend

    # Where backend is an object graph database...
    # examples are built on top of property graphs and
    # sources not natively graphed.
    #backend = kopernik.contrib.sensors.etcd.etcdproxy.BackendEtcd()
    peer = os.environ.get('NEO4J_PORT', 'http://localhost:7474/db/data/')
    peer_url_parts = urllib.parse.urlparse(peer)
    if peer_url_parts[0] == 'tcp':
        peer_url_parts[0] = 'http'
        peer = urllib.parse.urnunparse(peer_url_parts)

    backend = kopernik.backends.neo.driver.BackendNeo4j(peer)

    port = os.environ.get('KOPERNIK_PORT', 80)
    peer = os.environ.get('KOPERNIK_PEER', None)
    if peer:
        _register_with_peer(peer)
        while True:
            sleep(1)
    app.run(host='0.0.0.0', port=port, debug=True)
