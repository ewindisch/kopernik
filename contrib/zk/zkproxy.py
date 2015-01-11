import kazoo
import kopernik


class BackendZookeeper(kopernik.backend.CrudBackend):
    def __init__(self):
        self.zkconn = kazoo.KazooClient()
        self.zkconn.start()

    def create(self, key, data=None):
        if data:
            return self.zkconn.ensure_path(key)
        return self.zkconn.create(key, data, makepath=True)

    def read(self, key):
        return self.zkconn.get(key)

    def update(self, key, data):
        return self.zkconn.set(key, data)

    def delete(self, key):
        return self.zkconn.delete(key, recursive=True)

    def has_node(self, key):
        return self.zkconn.exists(key)


def main():
    kopernik.ServerCreate(
        backend=BackendZookeeper)


if __name__ == "__main__":
    main()
