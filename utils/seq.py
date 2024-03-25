import uuid


def gen_uuid():
    unique_id = uuid.uuid4()

    return str(unique_id)
