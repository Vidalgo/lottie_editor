from zlottie.base import LottieBase, LottieObjectMeta, LottieAttribute
from typing import Any, Dict, ForwardRef, Type
from enum import Enum

LottieObject = ForwardRef('LottieObject')


class LottieObject(LottieBase, metaclass=LottieObjectMeta):
    _attributes: Dict[str, LottieAttribute] = {}
    _attributes_by_tag: Dict[str, LottieAttribute] = {}
    __strict: bool = False

    def __init__(self, raw: Dict = None, **kwargs):
        if raw is not None:
            self.load(raw)
        else:
            if bad_kwarg := next((attr for attr in kwargs.keys() if attr not in self._attributes), None):
                raise TypeError(f"__init__() got an unexpected keyword argument '{bad_kwarg}'")
            self.__dict__.update(kwargs)

    def load(self, raw: Dict) -> None:
        for tag, value in raw.items():
            if tag not in self._attributes_by_tag:
                print('asdf')
            attribute = self._attributes_by_tag[tag]
            if attribute.autoload:
                if attribute.is_list:
                    value = [self._load_attribute(attribute=attribute, raw=r) for r in value]
                else:
                    value = self._load_attribute(attribute=attribute, raw=value)
                setattr(self, attribute.name, value)

    def to_raw(self) -> Dict:
        result = {}
        for name, attribute in self._attributes.items():
            value = self._value_to_dict(value=getattr(self, name))
            if value is not None:
                result[attribute.tag] = value
        return result

    @property
    def descriptor(self):
        return self._attributes

    @property
    def attributes(self):
        return {name: getattr(self, name) for name in self._attributes.keys()}

    @property
    def tags(self):
        return list(self._attributes_by_tag.keys())

    @staticmethod
    def _load_attribute(attribute: LottieAttribute, raw: Any):
        cls = attribute.type
        if issubclass(cls, LottieBase):
            cls = cls.get_load_class(raw=raw)
        return cls(raw)

    @staticmethod
    def _value_to_dict(value: Any) -> Dict:
        if isinstance(value, list) and len(value) > 0:
            return [LottieObject._value_to_dict(v) for v in value]
        elif isinstance(value, LottieBase):
            return value.to_raw()
        elif isinstance(value, Enum):
            return value.value
        else:
            return value
