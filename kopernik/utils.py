import uuid


host_uuid = uuid.uuid4()

def generate_urn():
    return uuid.uuid5(host_uuid, str(uuid.uuid4())).urn
