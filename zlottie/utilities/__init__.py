import shortuuid


def create_uuid(length: int = None) -> str:
    if length:
        return shortuuid.random(length=length)
    else:
        return shortuuid.uuid()
