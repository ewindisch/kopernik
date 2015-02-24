from collections import namedtuple
import flask
from flask import request
#import kopernik.contrib.sensors.etcd.etcdproxy
import kopernik.backends.neo.driver

app = flask.Flask(__name__)

"""
Object Graph Database Model
---------------------------

Tenants:
- All nodes in the graph are an object.
- All relationships in the graph are a node with a base relationship class.
- All objects implement a class.
- Classes are represented by nodes.
- Every node, class, and relationship is identified by a universally global URN:uuid.
- URNs are urn:kopernik:id:host
- URNs must have 'host' as last entry due to IPv6.


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


def _register_with_peer():
    """Registered with a peer"""
    #requests.post("http://parent/name", "")
    pass


@app.route("/nodes", methods=["GET"])
def get_nodes():
    #return flask.jsonify(list(backend.crud))
    return flask.jsonify(list(backend.nodes()))


@app.route("/node/<name>", methods=["GET"])
def node(name):
    nodes = backend.nodes()
    if name in nodes:
        return flask.jsonify(nodes[name])
    flask.abort(404)


@app.route("/node", methods=["POST"])
def create_node():
    properties = request.get_json(force=True)
    nodeURN = generate_urn()

    if not 'class_URN_str' in data:
        # Exception - no class specified
        flask.abort(400)

    classNode = kopernik.get_node(data['class_URN_str'])

    if not all([prop in properties for prop in classNode.properties]):
        # Interface not satisfied
        flask.abort(400)

    try:
        backend.create(nodeURN, properties)
    except Exception:
        flask.abort(500)
    return flask.jsonify(nodeURN)


@app.route("/node/<urn>", methods=["DELETE"])
def delete_node(urn):
    try:
        backend.delete(urn)
    except Exception:
        flask.abort(500)
    return flask.jsonify(urn)


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


if __name__ == "__main__":
    global backend

    # Where backend is an object graph database...
    # examples are built on top of property graphs and
    # sources not natively graphed.
    #backend = kopernik.contrib.sensors.etcd.etcdproxy.BackendEtcd()
    backend = kopernik.backends.neo.driver.BackendNeo4j()
    _register_with_peer()
    app.run(host='0.0.0.0', port=80, debug=True)
