from collections.abc import Iterator
from typing import List, Type, ForwardRef

LottieObject = ForwardRef('LottieObject')


class LottieIterator(Iterator):
    def __init__(self, root: LottieObject, **kwargs):
        self._root: LottieObject = root
        self._include_self: bool = kwargs.get('include_self', False)
        self._include_classes: List[Type] = kwargs.get('include_classes', [])
        self._exclude_classes: List[Type] = kwargs.get('exclude_classes', [])

    def __iter__(self):
        return self

    def __next__(self):
        if self._include_self:
            yield self._root
        for child in filter(vars(self), self._filter_child):
            yield child

    def _filter_child(self, attr):
        if not isinstance(attr, LottieBase):
            return False
        elif self._include_classes:
            return attr in self._include_classes
        else:
            return attr not in self._exclude_classes



