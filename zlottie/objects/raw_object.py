from zlottie.base import LottieObject
from typing import Dict
from copy import deepcopy


class RawObject(LottieObject):
    """raw object (i.e unparsed dictionary)"""

    def __init__(self, value: Dict = {}):
        self._value: Dict = value

    def load(cls, source):
        return RawObject(value=source)

    def to_dict(self):
        return self._value

    def clone(self):
        value = deepcopy(self._value)
        return self.load(value)
