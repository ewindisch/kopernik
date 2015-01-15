---------------------------------------
Kopernik
a peer for the Semantic Web-of-Things
---------------------------------------

This package provides an x86 Unix/POSIX/Linux service
for a kopernik-protocol compatible peer and inventory
service.

Peers of this service may be any device speaking the
kopernik protocol, such as other machines running this
service, or physical embedded devices running a kopernik
runtime environment.

---------------------------------------
Protocol Basics
---------------------------------------

Concepts & considerations of the Kopernik Protocol

1. Device nodes will run an agent and register themselves to another node
2. Some nodes will act purely as a hub for other nodes
3. Some nodes may not natively speak the kopernik protocol.
4. Connectivity between nodes forms a distributed model for inventory and discovery.

---------------------------------------
Sensors
---------------------------------------

Physical devices generally include sensors. The kopernik pc service
allows two forms of sensors:

1. Backend service sensors, proxying to other inventory systems or databases. For instance, etcd and zookeeper integration provides transparency into systems and data available on those systems, exposed as sensor data.
2. Connected peers. These are registered peers which provide their own direct-attached sensors, or perhaps are themselves hubs to their own registered peers containing directly attached sensors.

---------------------------------------
Databases
---------------------------------------

The Kopernik service supports two major types of databases: caching servers and datastores.

Caching servers provide quick retrieval of commonly accessed data, especially of data which is non-local and retrieved on behalf of a proxied system. This works similar to DNS. A query is performed which recurses through Kopernik to a remote, authoritative node. A TTL is provided on the response and we may cache the response for up to the specified number of milliseconds.

Datastores are used for data stored directly in Kopernik. Typically, in-memory data storage is sufficient for system inventories, but other datastores may be useful for scalable installations.

---------------------------------------
Scaling
---------------------------------------

For most peers, a single device is necessary, as it describes the peer itself and its own local data. However, hub machines also exist. While they're peers, they're peers operating as a hub and aggregator for many other systems. This typically will happen for systems representing a "thing" such as an organization. For instance, a node represents your organization to which many other nodes belong, such as employees, systems, devices, and various intangibles. These things are all registered to each other and ultimately up to the organization. Expanding upon this, a phone is registered to an employee, with the employee registered to the organization.

At some point, something as large as an organization will need scalability and reliability. For this reason, Kopernik allows operating a node across multiple peers. Data consistency is managed through a single, pluggable datastore.

---------------------------------------
License: Proprietary
---------------------------------------
It is intended that all or part of this will become opensource as it is matured into an MVP.
