import requests
import flask
from flask import Flask
import json
import time

app = Flask(__name__)
app.debug = True
request = flask.globals.request
session = flask.globals.session

nodes = set()
relationships = {}

def register_with_parent():
    #requests.post("http://parent/name", "")
    pass

def flush_expired():
    def expired_nodes():
        for n in nodes:
            if relationships.get((n, 'expiration_time'), 0) <= time.time():
                print relationships.get((n, 'expiration_time'), 0)
                print time.time()
                try:
                    yield n
                except:
                    pass
    expired = list(expired_nodes())
    for n in expired:
        nodes.remove(n)
        del relationships[(n, 'expiration_time')]
 
@app.route("/nodes", methods=["GET"])
def list_nodes():
    #def is_expired(n):
    #    return relationships.get((n, 'expiration_time')) <= time.time() 
    #anodes = filter(is_expired, nodes)
    flush_expired()
    return json.dumps(list(nodes)) + "\n"

@app.route("/node/<name>", methods=["GET"])
def info(name):
    try:
        return nodes[name] + "\n"
    except:
        flask.abort(404)

@app.route("/node/<name>", methods=["POST"])
def register(name):
    #if not 'username' in session:
    #    flask.abort(401)
    try:
        expire_at = int(request.form.get('expire_at', time.time() + 300))
        relationships.update({(name, 'expiration_time'): expire_at})
        nodes.add(name)
    except:
        flask.abort(500)
    return name + "\n"

@app.route("/node/<node_name>/<node2_name>/relationship/<attribute>", methods=["POST"])
def create_relationship(node_name, node2_name, attribute):
    #if not 'username' in session:
    #    abort(401)
    #try:
    s = [node_name, node2_name]
    s.sort()
    relationships.update({tuple(s): attribute})
    #except:
    #    flask.abort(500)
    return str(s + [attribute]) + "\n"

@app.route("/node/<name>", methods=["DELETE"])
def unregister(name):
    if not 'username' in session:
        abort(401)
    try:
        nodes.remove(name)
        return name + "\n"
    except:
        flask.abort(500)

@app.route('/login', methods=["POST"])
def login():
    if request.method == 'POST':
            session['username'] = request.form['username']
            return redirect(url_for('index'))
    abort(401)

if __name__ == "__main__":
    register_with_parent()
    app.run()
