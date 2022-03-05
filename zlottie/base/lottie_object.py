from abc import ABC
from typing import List
from zlottie.base import LottieAttribute


class LottieObjectMeta(type):
    def __new__(cls, name, bases, attrs):
        attributes = LottieObjectMeta._prepare_lottie_attributes(attrs)
        attrs['_attributes'] = attributes
        attrs['__init__'] = LottieObjectMeta._autoinit
        for k in attributes.keys():
            attrs[k] = None
        return super().__new__(cls, name, bases, attrs)

    @staticmethod
    def _autoinit(lottie_object, **kwargs):
        kwargs = {k: v for k, v in kwargs.items() if k in lottie_object._attributes}
        vars(lottie_object).update(kwargs)

    @staticmethod
    def _prepare_lottie_attributes(attrs):
        annotations = attrs.get('__annotations__', {})
        attributes = {k: v for k, v in attrs.items() if isinstance(v, LottieAttribute)}
        for k, v in attributes.items():
            type = annotations.get(k)
            attributes[k] = v.clone(type=type)
        return attributes


class LottieObject(metaclass=LottieObjectMeta):
    _attributes: List[LottieAttribute] = []

    def load(self, source):
        pass

    def to_dict(self):
        return {}

    def clone(self):
        pass

    @property
    def attributes(self):
        return self._attributes
