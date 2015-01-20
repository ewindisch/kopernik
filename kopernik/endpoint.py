from collections import namedtuple
import flask
import kopernik.contrib.sensors.etcd.etcdproxy

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
- URNs are global and registered via blockchain.
- URN queries may be handled via DNS proxy.

"""

"""
Classes
"""
ClassStruct = namedtuple(
    "Class",
    (
        "URN_str",
        "name_str",
        "class_URN_str",
    )
)

"""
Define the "keyword" classes
"""
BaseObjectObject = ClassStruct(
    'urn:uuid:2c53c60b-65a9-479d-905a-3ff45ab400a3',
    'object',
    # Is an object; self-referential...
    'urn:uuid:2c53c60b-65a9-479d-905a-3ff45ab400a3')

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

"""
Define root node
"""
RootObject = ObjectStruct(
    "urn::uuid:74d38813-2959-4a4e-9ae0-413297290108",
    "ROOT",
    # Is an object
    "urn:uuid:2c53c60b-65a9-479d-905a-3ff45ab400a3"
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
Define the keyword relationships
"""
BaseRelationshipObject = ObjectStruct(
    'urn:uuid:32401dc0-bdc4-4bb5-a8ed-047f3922b169',
    'relationship',
    # Is an object
    'urn:uuid:2c53c60b-65a9-479d-905a-3ff45ab400a3',
)
BaseRelationship = RelationshipStruct(
    'urn:uuid:1fe94c42-0395-43c9-97a5-4fb83e0b637c',
    'RELATIONSHIP',
    # Is a Relationship
    'urn:uuid:32401dc0-bdc4-4bb5-a8ed-047f3922b169',

    # self -> ROOT
    'urn:uuid:1fe94c42-0395-43c9-97a5-4fb83e0b637c',
    'urn:uuid:74d38813-2959-4a4e-9ae0-413297290108'
)

def __init__(self):
    pass


def _register_with_peer():
    """Registered with a peer"""
    #requests.post("http://parent/name", "")
    pass


@app.route("/nodes", methods=["GET"])
def get_nodes():
    return flask.jsonify(list(backend.crud))


@app.route("/node/<name>", methods=["GET"])
def node(name):
    nodes = backend.nodes()
    if name in nodes:
        return flask.jsonify(nodes[name])
    flask.abort(404)


@app.route("/node/<name>", methods=["POST"])
def create_node(nodeName):
    data = getdata()
    nodeClass = data['class_URN_str']
    nodeURN = generate_urn()

    try:
        backend.create(nodeURN, nodeClass, nodeName)
    except Exception:
        flask.abort(500)
    return flask.jsonify(name)


@app.route("/node/<name>", methods=["DELETE"])
def delete_node(name):
    try:
        backend.delete(name)
    except Exception:
        flask.abort(500)
    return flask.jsonify(name)


@app.route("/node/<name>/property/<pname>", methods=["GET"])
def node_property(name, pname):
    node_properties = backend.node(name).properties
    return flask.jsonify(node_properties)
    flask.abort(404)


@app.route("/node/<name>/property/<pname>", methods=["POST"])
def create_node_property(name, pname):
    try:
        backend.create(name)
    except Exception:
        flask.abort(500)
    return flask.jsonify(name)


@app.route("/node/<name>/property/<pname>", methods=["DELETE"])
def delete_node_property(name):
    try:
        backend.delete(name)
    except Exception:
        flask.abort(500)
    return flask.jsonify(name)


@app.route("/node/<node_name>/<node2_name>/relationship/<attribute>",
           methods=["POST"])
def create_relationship(node_name, node2_name, attribute):
    s = [node_name, node2_name]
    s.sort()
    s += [attribute]
    return flask.jsonify(s)


if __name__ == "__main__":
    global backend

    # Where backend is an object graph database...
    # examples are built on top of property graphs and
    # sources not natively graphed.
    backend = kopernik.contrib.sensors.etcd.etcdproxy.BackendEtcd()
    _register_with_peer()
    app.run()
