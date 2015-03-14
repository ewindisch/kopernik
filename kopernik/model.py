"""
Object Graph Database Model
---------------------------

Tenants:
- All nodes in the graph are an object.
- All relationships in the graph are a node with a base relationship class.
- All objects implement a class.
- Classes are represented by nodes.
- Every node, class, and relationship is identified by a universally global URN:uuid.
- URNs use UUID urn syntax.


"""

"""
All nodes are objects...
"""
ObjectStruct = namedtuple(
    "Object",
    (
        "URN_str",
        "name_str",
        "class_URN_str",
    )
)
ClassStruct = namedtuple(
    "Object",
    (
        "URN_str",
        "name_str",
        "class_URN_str",
    )
)


"""
All relationships are objects... and thus nodes
"""
RelationshipStruct = namedtuple(
    "Relationship",
    (
        "URN_str",
        "name_str",
        "class_URN_str", # type of relationship...

        "node1_URN_str",
        "node2_URN_str"
    )
)

"""
Global object Object...
"""
BaseObjectObject = ClassStruct(
    'urn:kopernik:object:::1',
    'object',
    # Is an object; self-referential...
    'urn:kopernik:object:::1'
)
#graph.register(BaseObjectObject)

"""
Global root node
"""
RootObject = ObjectStruct(
    "urn:kopernik:root:::1",
    "Graph Root",
    # Is an object
    "urn:kopernik:object:::1"
)
#graph.register(RootObject)

"""
Define the keyword relationships
"""
BaseRelationshipObject = ObjectStruct(
    'urn:kopernik:relationship:::1',
    'Relationship Object',
    # Is an object
    'urn:kopernik:object:::1',
)
#graph.register(BaseRelationshipObject)

BaseRelationship = RelationshipStruct(
    'urn:kopernik:relationship_to_root:::1',
    'RELATIONSHIP',
    # Is a Relationship
    'urn:kopernik:relationship:::1',

    # self -> ROOT
    'urn:kopernik:root:::1',
    'urn:kopernik:relationship:::1'
)
#graph.register(BaseRelationship)
