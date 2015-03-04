import py2neo


# Support running in Docker; Presume container hostname is docker-neo4j (this is what we set in docker compose)
py2neo.rewrite(("http", 'docker-neo4j', 7474), ("http", "localhost", 7474))

class BackendNeo4j(object):
    def __init__(self):
        self.graph = py2neo.Graph()

    def nodes(self, limit=5):
        graph = self.graph
        query = "MATCH (n:KopernikNode) RETURN n"
        if limit:
            query += " LIMIT %i" % (limit,)
        result_iter = graph.cypher.stream(query)
        for result in result_iter:
            yield result[0]['id']

    def _get_node(self, node_id):
        graph = self.graph
        result = graph.cypher.execute("MATCH (n:KopernikNode {id:\"%s\"}) RETURN n LIMIT 1" % (node_id,))
        return result.one

    def node(self, node_id):
        result = self._get_node(node_id)
        if result:
            return result.properties
        return None

    def create(self, nodeURN, properties):
        graph = self.graph
        node = py2neo.Node("KopernikNode", id=nodeURN)
        try:
            for k,v in properties.iteritems():
                node.properties[k] = v
        except Exception:
            print >>stderr, "properties: %s" % (properties)
            raise
        graph.create(node)

    def delete(self, node_id):
        result = self._get_node(node_id)
        graph = self.graph
        graph.delete(result)
        return True
