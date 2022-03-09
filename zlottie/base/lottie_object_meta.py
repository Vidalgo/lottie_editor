from typing import Any, ForwardRef
from zlottie.base import LottieAttribute

LottieObject = ForwardRef('LottieObject')


class LottieObjectMeta(type):
    def __new__(cls, type_name, bases, attrs):
        attributes = LottieObjectMeta._prepare_lottie_attributes(cls, type_name, bases, attrs)
        attrs.update({k: None for k in attributes.keys()})
        attrs.setdefault('__init__', LottieObjectMeta._autoinit)
        attrs['_attributes'] = attributes
        attrs['_attributes_by_tag'] = {attr.tag: attr for name, attr in attributes.items()}
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
            own_attributes[name] = attr.clone(name=name, annotation=annotation)
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
