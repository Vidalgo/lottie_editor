from typing import Dict, Any, ForwardRef
from zlottie.base import LottieAttribute

LottieObject = ForwardRef('LottieObject')


class LottieObjectMeta(type):
    def __new__(cls, type_name, bases, attrs):
        attributes = LottieObjectMeta._prepare_lottie_attributes(cls, type_name, bases, attrs)
        attrs['_attributes'] = attributes
        for k in attributes.keys():
            attrs[k] = None
        if '__init__' not in attrs:
            attrs['__init__'] = LottieObjectMeta._autoinit
        return super().__new__(cls, type_name, bases, attrs)

    @staticmethod
    def _autoinit(obj: LottieObject, **kwargs):
        if bad_attr := next((attr for attr in kwargs.keys() if attr not in obj._attributes), None):
            raise f"TypeError: _autoinit() got an unexpected keyword argument '{bad_attr}'"
        vars(obj).update(kwargs)

    @staticmethod
    def _prepare_lottie_attributes(cls, type_name, bases, attrs):
        print(attrs)
        # lottie attributes from current class
        own_attributes = {k: v for k, v in attrs.items() if isinstance(v, LottieAttribute)}
        own_annotations = attrs.get('__annotations__', {})
        for name, attr in own_attributes.items():
            annotation = own_annotations.get(name, Any)
            own_attributes[name] = attr.clone(type=annotation)
        # lottie attributes from base classes
        attributes = {}
        for base in bases:
            if type(base) == cls:
                attributes.update(base._attributes)
        # override base with current
        attributes.update(own_attributes)
        return attributes

    @staticmethod
    def _null_func(obj, *args, **kwargs):
        pass


class LottieObject(metaclass=LottieObjectMeta):
    _attributes: Dict[str, LottieAttribute] = {}

    def load(self, source):
        pass

    def to_dict(self):
        return {}

    def clone(self):
        pass

    @property
    def attributes(self):
        return self._attributes
