import py2neo

class BackendNeo4j(object):
    def nodes(self):
        graph = py2neo.Graph()
        return graph.cypher.execute("MATCH n RETURN n")

    def create(nodeURN, properties):
        node = py2neo.Node(nodeURN)
        for k,v in data:
            node.properties[k] = v
        py2neo.create(node)

