import py2neo


# Support running in Docker; Presume container hostname is docker-neo4j (this is what we set in docker compose)
py2neo.rewrite(("http", 'docker-neo4j', 7474), ("http", "localhost", 7474))

class BackendNeo4j(object):
    def __init__(self, host):
        self._graph_host = host

    def _graph(self):
        return py2neo.Graph(self._graph_host)

    def nodes(self, limit=5):
        graph = self._graph()
        query = "MATCH (n:KopernikNode) RETURN n"
        if limit:
            query += " LIMIT %i" % (limit,)
        result_iter = graph.cypher.stream(query)
        for result in result_iter:
            yield result[0]['id']

    def _get_node(self, node_id):
        graph = self._graph()
        query = "MATCH (n:KopernikNode {{id:\"{}\"}}) RETURN n LIMIT 1".format(node_id)
        result = graph.cypher.execute(query)
        #"MATCH (n:KopernikNode {id:\"{}\"}) RETURN n LIMIT 1".format(node_id))
        return result.one

    def node(self, node_id):
        result = self._get_node(node_id)
        if result:
            return result.properties
        return None

    def create(self, nodeURN, properties):
        graph = self._graph()
        node = py2neo.Node("KopernikNode", id=nodeURN)
        try:
            for k,v in properties.items():
                node.properties[k] = v
        except Exception:
            print("properties: {}".format(properties))
            raise
        graph.create(node)

    def delete(self, node_id):
        result = self._get_node(node_id)
        graph = self._graph()
        graph.delete(result)
        return True
