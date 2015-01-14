Mapper for Kopernik + etcd
--------------------------

Allows access to etcd data via kopernik.

Because kopernik is a graph database
and etcd is both a host inventory AND a
key-value store, we have more than one
way of representing the data. That is,
the data can be natively transported,
but in Kopernik, machines are data as well.

Thus, mapping is provided. A default mapping
should be sufficient for most users, but this
is configurable for most use-cases.

This information is liable to change, if it is
not already outdated (it probably is)
