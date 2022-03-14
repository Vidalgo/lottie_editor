from collections.abc import Iterator
from typing import List, Type
from zlottie.base.lottie_object import LottieObject


class LottieIterator(Iterator):
    def __init__(self, root: LottieObject, **kwargs):
        filter = self._create_filter(**kwargs)
        children = [root] if kwargs.get('include_self', False) else self._get_children(root)
        self.__iter = self._iter(children=children, filter=filter)

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.__iter)

    @staticmethod
    def _iter(children, filter) -> Iterator:
        for child in children:
            if filter(child):
                yield child
            grandchildren = LottieIterator._get_children(child)
            for descendant in LottieIterator._iter(children=grandchildren, filter=filter):
                yield descendant

    @staticmethod
    def _create_filter(**kwargs):
        filters = []
        filters.append(lambda c: isinstance(c, LottieObject))
        if classes := kwargs.get('include_classes'):
            filters.append(lambda c: type(c) in classes)
        if classes := kwargs.get('exclude_classes'):
            filters.append(lambda c: type(c) not in classes)
        return lambda c: all(f(c) for f in filters)

    @staticmethod
    def _get_children(obj: LottieObject) -> List[LottieObject]:
        children = []
        for value in obj.attributes.values():
            if isinstance(value, LottieObject):
                children.append(value)
            elif isinstance(value, List):
                children.extend(v for v in value if isinstance(v, LottieObject))
        return children

