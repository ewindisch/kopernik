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
import kopernik.utils


app = flask.Flask(__name__)

host_uuid = kopernik.utils.host_uuid



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
    nodeURN = kopernik.utils.generate_urn()

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
