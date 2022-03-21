from zlottie.base import LottieBase
from typing import Dict
from copy import deepcopy


class RawLottieObject(LottieBase):
    """raw object (i.e unparsed dictionary)"""

    def __init__(self, raw: Dict = {}, **kwargs):
        super().__init__(**kwargs)
        self._raw: Dict = raw

    def load(self, source: Dict):
        self._raw = source

    def dump(self):
        return self._raw

    def clone(self):
        value = deepcopy(self._raw)
        return self.load(value)

    # MutableMapping API
    def __getitem__(self, key):
        return self._raw.__getitem__(key)

    def __setitem__(self, key, value):
        self._raw.__setitem__(key, value)

    def __delitem__(self, key):
        self._raw.__delitem__(key)

    def __iter__(self):
        return self._raw.__iter__()

    def __len__(self):
        return self._raw.__len__()

    def __repr__(self):
        return repr(self._raw)

    def keys(self):
        return self._raw.keys()

    def values(self):
        return self._raw.values()

    def items(self):
        return self._raw.items()

    def get(self, *args, **kwargs):
        return self._raw.get(*args, **kwargs)

    def clear(self):
        """ D.clear() -> None.  Remove all items from D. """
        pass

    def copy(self):
        """ D.copy() -> a shallow copy of D """
        pass

    def pop(self, k, d=None):
        return self._raw.pop(k, d)

    def popitem(self, *args, **kwargs):
        return self._raw.popitem(*args, **kwargs)

    def setdefault(self, *args, **kwargs):
        return self._raw.setdefault(*args, **kwargs)

    def update(self, E=None, **F):
        self._raw.update(E, **F)
