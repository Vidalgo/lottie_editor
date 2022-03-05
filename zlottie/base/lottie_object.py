from abc import ABC
from typing import List
from zlottie.base import LottieAttribute


class LottieObjectMeta(type):
    def __new__(cls, name, bases, attr):
        annotations = attr.get('__annotations__', {})
        _attributes = {k: v for k, v in attr.items() if isinstance(v, LottieAttribute)}
        for k, v in _attributes.items():
            type = annotations.get(k)
            _attributes[k] = LottieAttribute.copy(v, type=type)
        attr['_attributes'] = _attributes
        return super().__new__(cls, name, bases, attr)


class LottieObject(metaclass=LottieObjectMeta):
    _attributes: List[LottieAttribute] = []

    def __init__(self):
        pass

    def load(self, source):
        pass

    def to_dict(self):
        return {}

    def clone(self):
        pass

    @property
    def attributes(self):
        return self._attributes
