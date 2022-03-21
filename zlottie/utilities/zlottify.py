from zlottie.base import LottieObject
from zlottie.iterators import LottieIterator
from zlottie.utilities import create_uuid


def add_ids(root: LottieObject, override_existing: bool = False) -> LottieObject:
    filter_ = lambda o: hasattr(o, 'id')
    iterator = LottieIterator(root, filter=filter_)
    for lottie_object in iterator:
        if not lottie_object.id or override_existing:
            lottie_object.id = create_uuid()
    return root
