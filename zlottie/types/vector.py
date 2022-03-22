from zlottie.base import LottieBase
from collections.abc import MutableSequence
import operator
import math
from typing import List, Any, Dict
from numbers import Number


class Vector(LottieBase, MutableSequence):
    def __init__(self, *args):
        self._components = list(args)
        self._type = type(self)

    # LottieBase
    def load(self, raw: List[Number]) -> None:
        self._components = list(raw)

    def dump(self) -> Dict:
        return self.to_list()

    def clone(self):
        raise NotImplementedError('TODO')

    # MutableSequence
    def __getitem__(self, key):
        if isinstance(key, slice):
            return Vector(*self._components[key])
        return self._components[key]

    def __setitem__(self, key, value):
        self._components[key] = value

    def __delitem__(self, key):
        self._components.__delitem__(key)

    def __len__(self):
        return len(self._components)

    def insert(self, index: int, value: Any) -> None:
        self._components.insert(index, value)

    # Math
    def __add__(self, other):
        return self._apply(operator.add, other)

    def __sub__(self, other):
        return self._apply(operator.sub, other)

    def __mul__(self, other):
        return self._apply(operator.mul, other)

    def __truediv__(self, other):
        return self._apply(operator.truediv, other)

    def __floordiv__(self, other):
        return self._apply(operator.floordiv, other)

    def __neg__(self):
        return self._apply_unitary(operator.neg)

    def __eq__(self, other):
        return self._type == type(other) and self._components == other._components

    def __abs__(self):
        return self._apply_unitary(operator.abs)

    # make right-side arithmetic work (i.e. v + 3 == 3 + v)
    __radd__ = __add__
    __rsub__ = __sub__
    __rmul__ = __mul__
    __rtruediv__ = __truediv__
    __rfloordiv__ = __floordiv__

    def _apply(self, op, other):
        if isinstance(other, Vector):
            return self._type(*map(op, self._components, other._components))  # component-wise
        else:
            return self._type(*(op(c, other) for c in self._components))  # broadcast

    def _apply_unitary(self, op):
        return self._type(*(op(c) for c in self._components))

    # other
    def __str__(self):
        return str(self._components)

    def __repr__(self):
        return "Vector(%s)" % ", ".join(map(str, self))

    def to_list(self) -> List:
        return list(self._components)


if __name__ == '__main__':
    v = Vector(1,2,3)
    print(v + 3)
    print(3 + v)
    print(v + v)
    print('asdf')
