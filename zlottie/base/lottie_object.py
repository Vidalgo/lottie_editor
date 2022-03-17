from zlottie.base import LottieBase, LottieObjectMeta, LottieAttribute, RawLottieObject
from typing import Any, Dict, ForwardRef, Type
from enum import Enum

import logging

logger = logging.getLogger(__name__)

LottieObject = ForwardRef('LottieObject')


class LottieObject(LottieBase, metaclass=LottieObjectMeta):
    _attributes: Dict[str, LottieAttribute] = {}
    _attributes_by_tag: Dict[str, LottieAttribute] = {}
    __strict: bool = False

    def __init__(self, raw: Dict = None, **kwargs):
        super().__init__(**kwargs)
        self._extra: RawLottieObject = RawLottieObject()
        if raw is not None:
            self.load(raw)
        else:
            self._init_from_kwargs(**kwargs)

    def load(self, raw: Dict) -> None:
        known_tags_values = {tag: raw[tag] for tag in (raw.keys() & self.tags)}     # set intersection
        extra_tags_values = {tag: raw[tag] for tag in (raw.keys() - self.tags)}     # set difference
        attributes_values = {}
        for tag, value in known_tags_values.items():
            attribute = self._attributes_by_tag[tag]
            if attribute.autoload:
                if attribute.is_list:
                    value = [self._load_attribute(attribute=attribute, raw=r, path=self.path, index=idx) for idx, r in enumerate(raw[tag])]
                else:
                    value = self._load_attribute(attribute=attribute, path=self.path, raw=raw[tag])
                attributes_values[attribute.name] = value
        self.__dict__.update(attributes_values)
        self._extra = RawLottieObject(raw=extra_tags_values)
        if extra_tags_values:
            logger.warning(f'found extra properties in {self.path}: {set(extra_tags_values.keys())}')

    def dump(self) -> Dict:
        result = {}
        for name, attribute in self._attributes.items():
            value = self._value_to_raw(value=getattr(self, name))
            if value != attribute.default or attribute.always_dump:
                result[attribute.tag] = value
        result.update(self._extra)
        return result

    @property
    def descriptor(self):
        return self._attributes

    @property
    def attributes(self):
        return {name: getattr(self, name) for name in self._attributes.keys()}

    @property
    def tags(self):
        return set(self._attributes_by_tag.keys())

    @property
    def extra(self):
        return self._extra

    @staticmethod
    def _load_attribute(attribute: LottieAttribute, raw: Any, path: str, index: int = None):
        cls = attribute.type
        if issubclass(cls, LottieBase):
            cls = cls.get_load_class(raw=raw)
            tag = attribute.tag if index is None else f"{attribute.tag}[{index}]"
            path = f"{path}['{attribute.tag}']" if index is None else f"{path}['{attribute.tag}'][{index}]"
            return cls(raw, tag=tag, path=path)
        else:
            return cls(raw)

    @staticmethod
    def _value_to_raw(value: Any) -> Dict:
        if isinstance(value, list) and value:
            return [LottieObject._value_to_raw(v) for v in value]
        elif isinstance(value, LottieBase):
            return value.dump()
        elif isinstance(value, Enum):
            return value.value
        elif isinstance(value, bool):
            return int(value)
        else:
            return value

    def _init_from_kwargs(self, **kwargs):
        if bad_kwarg := next((attr for attr in kwargs.keys() if attr not in self._attributes), None):
            raise TypeError(f"__init__() got an unexpected keyword argument '{bad_kwarg}'")
        self.__dict__.update(kwargs)
