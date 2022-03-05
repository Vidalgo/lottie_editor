from typing import Dict, Any, ForwardRef
from zlottie.base import LottieAttribute

LottieObject = ForwardRef('LottieObject')


class LottieObjectMeta(type):
    def __new__(cls, type_name, bases, attrs):
        attributes = LottieObjectMeta._prepare_lottie_attributes(cls, type_name, bases, attrs)
        attrs.update({k: None for k in attributes.keys()})
        attrs.setdefault('__init__', LottieObjectMeta._autoinit)
        attrs['_attributes'] = attributes
        attrs['_tags'] = {attr.tag: attr for name, attr in attributes.items()}
        return super().__new__(cls, type_name, bases, attrs)

    @staticmethod
    def _autoinit(obj: LottieObject, **kwargs):
        if bad_attr := next((attr for attr in kwargs.keys() if attr not in obj._attributes), None):
            raise TypeError(f"_autoinit() got an unexpected keyword argument '{bad_attr}'")
        vars(obj).update(kwargs)

    @staticmethod
    def _prepare_lottie_attributes(cls, type_name, bases, attrs):
        # lottie attributes from current class
        own_attributes = {k: v for k, v in attrs.items() if isinstance(v, LottieAttribute)}
        own_annotations = attrs.get('__annotations__', {})
        for name, attr in own_attributes.items():
            annotation = own_annotations.get(name, Any)
            own_attributes[name] = attr.clone(name=name, type=annotation)
        # lottie attributes from base classes
        attributes = {}
        for base in bases:
            if type(base) == cls:
                attributes.update(base._attributes)
        # override base with current
        attributes.update(own_attributes)
        # assert tags are unique
        tags = set(attr.tag for attr in attributes.values())
        if len(tags) != len(attributes):
            raise TypeError("attribute tags must be unique")
        return attributes

    @staticmethod
    def _null_func(obj, *args, **kwargs):
        pass


class LottieObject(metaclass=LottieObjectMeta):
    _attributes: Dict[str, LottieAttribute] = {}
    _tags: Dict[str, str] = {}

    @classmethod
    def load(cls, source):
        pass

    def to_dict(self):
        return {}

    def clone(self):
        pass

    @property
    def attributes(self):
        return self._attributes

    @property
    def tags(self):
        return self._tags

    def __setattr__(self, key, value):
        if key in self._attributes:
            self._set_lottie_attr(key, value)
        else:
            super().__setattr__(key, value)

    def _set_lottie_attr(self, key, value):
        # TODO: add type validation
        super().__setattr__(key, value)

    def _load_attribute(self, name, value):
        setattr(self, name, value)