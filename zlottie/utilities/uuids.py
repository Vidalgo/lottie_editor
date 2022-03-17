import shortuuid


def create_uuid(length: int = None) -> str:
    if length:
        return shortuuid.random(length=length)
    else:
        return shortuuid.uuid()


def append_uuid(tag: str, length: int = 8, separator: str = '#'):
    return f'{tag}{separator}{create_uuid(length=length)}'
