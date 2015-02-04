import py2neo

class BackendNeo(object):
    def nodes(self):
        return cypher("MATCH n RETURN n")

    def create(nodeURN, properties)
        node = py2neo.Node(nodeURN)
        for k,v in data:
            node.properties[k] = v
        py2neo.create(node)

