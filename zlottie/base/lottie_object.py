from zlottie.base import LottieAttribute
from zlottie.base.lottie_object_meta import LottieObjectMeta
from typing import Dict


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