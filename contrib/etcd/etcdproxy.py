import etcd
import kopernik


class BackendEtcd(kopernik.backend.CrudBackend):
    def __init__(self):
        self._etcd_client = etcd.Client()

    def _get_nodes(self):
        machines = client.machines
        nodes = {node: {} for node in machines}
        nodes[client.leader] = {'leader': True}
        return nodes

    def read(self, key):
        return self._get_nodes().get(key, None)

    def has_node(self, key):
        return key in self._etcd_client.machines


def main():
    kopernik.ServerCreate(
        backend=BackendEtcd)


if __name__ == "__main__":
	main()
