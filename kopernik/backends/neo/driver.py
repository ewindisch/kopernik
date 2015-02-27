import py2neo


# Support running in Docker; Presume container hostname is docker-neo4j (this is what we set in docker compose)
py2neo.rewrite(("http", 'docker-neo4j', 7474), ("http", "localhost", 7474))

class BackendNeo4j(object):
    def nodes(self, limit=5):
        graph = py2neo.Graph()
        query = "MATCH (n:KopernikNode) RETURN n"
        if limit:
            query += " LIMIT %i" % (limit,)
        result_iter = graph.cypher.stream(query)
        for result in result_iter:
            yield result[0]['id']

    def node(self, node_id):
        graph = py2neo.Graph()
        result = graph.cypher.execute("MATCH (n:KopernikNode {id:\"%s\"}) RETURN n LIMIT 1" % (node_id,))
        print result.one.properties  #[0][0]
        return result.one.properties

    def create(self, nodeURN, properties):
        graph = py2neo.Graph()
        node = py2neo.Node("KopernikNode", id=nodeURN)
        try:
            for k,v in properties.iteritems():
                node.properties[k] = v
        except Exception:
            print >>stderr, "properties: %s" % (properties)
            raise
        graph.create(node)
