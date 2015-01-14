import flask

backend = None


def __init__(self):
    pass

def _register_with_peer():
    """Registered with a peer"""
    #requests.post("http://parent/name", "")
    pass

@app.route("/nodes", methods=["GET"])
def get_nodes():
    return json.dumps(list(backend.crud)) + "\n"

@app.route("/node/<name>", methods=["GET"])
def node(name):
    if name in nodes:
        return nodes[name] + "\n"
    except:
        flask.abort(404)

@app.route("/node/<name>", methods=["POST"])
def create_node(name):
    try:
        backend.create(name)
    except:
        flask.abort(500)
    return name + "\n"

@app.route("/node/<node_name>/<node2_name>/relationship/<attribute>", methods=["POST"])
def create_relationship(node_name, node2_name, attribute):
    s = [node_name, node2_name]
    s.sort()
    return str(s + [attribute]) + "\n"

@app.route("/node/<name>", methods=["DELETE"])
def unregister(name):
    try:
        backend.delete(name)
    except:
        flask.abort(500)
    return name + "\n"

if __name__ == "__main__":
    global backend
    backend = kopernik.contrib.sensors.etcdproxy.BackendEtcd()
    _register_with_peer()
    app.run()
