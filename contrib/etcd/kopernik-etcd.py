import etcd

def main():
	client = etcd.Client()

	nodes/ ->
	m = client.machines()
	nodes = {n => {} for n in m}
	nodes[client.leader] = {'leader': True}

if __name__ == "__main__":
	main()
