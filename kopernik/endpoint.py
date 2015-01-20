import flask
import kopernik.contrib.sensors.etcd.etcdproxy

app = flask.Flask(__name__)


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
def create_node(name):
    try:
        backend.create(name)
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
    backend = kopernik.contrib.sensors.etcd.etcdproxy.BackendEtcd()
    _register_with_peer()
    app.run()
