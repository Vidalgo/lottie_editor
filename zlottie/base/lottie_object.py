from zlottie.base import LottieAttribute
from zlottie.base.lottie_object_meta import LottieObjectMeta
from typing import Any, Dict, ForwardRef
from enum import Enum

LottieObject = ForwardRef('LottieObject')


class LottieObject(metaclass=LottieObjectMeta):
    _attributes: Dict[str, LottieAttribute] = {}
    _attributes_by_tag: Dict[str, LottieAttribute] = {}
    __strict: bool = False

    def load(self, raw: Dict) -> None:
        for tag, value in raw.items():
            attribute = self._attributes_by_tag[tag]
            if attribute.is_list:
                value = [self._load_single_attribute(attribute=attribute, raw=r) for r in value]
            else:
                value = self._load_single_attribute(attribute=attribute, raw=value)
            setattr(self, attribute.name, value)

    def to_dict(self) -> Dict:
        result = {}
        for name, attribute in self._attributes.items():
            value = self._single_value_to_dict(value=getattr(self, name))
            if value is not None:
                result[attribute.tag] = value
        return result

    @classmethod
    def from_dict(cls, raw: Dict) -> LottieObject:
        obj = cls()
        obj.load(raw=raw)
        return obj

    def clone(self):
        pass

    @property
    def attributes(self):
        return self._attributes

    @property
    def tags(self):
        return list(self._attributes_by_tag.keys())

    def __setattr__(self, key, value):
        if key in self._attributes:
            self._set_lottie_attr(key, value)
        else:
            super().__setattr__(key, value)

    @staticmethod
    def _load_single_attribute(attribute: LottieAttribute, raw: Dict):
        cls = attribute.type
        if isinstance(cls, LottieObject):
            value = cls()
            value.load(raw)
            return value
        else:
            return cls(raw)

    @staticmethod
    def _single_value_to_dict(value: Any) -> Dict:
        if isinstance(value, list) and len(value) > 0:
            return [LottieObject._single_value_to_dict(v) for v in value]
        elif isinstance(value, LottieObject):
            return value.to_dict()
        elif isinstance(value, Enum):
            return value.value
        else:
            return value

    def _set_lottie_attr(self, key, value):
        # TODO: add type validation
        super().__setattr__(key, value)

    def _load_attribute(self, name, value):
        setattr(self, name, value)

