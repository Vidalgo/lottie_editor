from collections.abc import Iterator
from typing import List, Type, Callable
from zlottie.base.lottie_object import LottieObject


# Annotations
LottieObjectFilter = Callable[[LottieObject], bool]
LottieObjectIterator = Iterator[Type[LottieObject]]


class LottieIterator(Iterator):
    def __init__(self, root: LottieObject, include_self: bool = False, **kwargs):
        """create a new pre-order lottie iterator

        Args:
            root (LottieObject): root node
            include_self (bool): (optional) should iterator return the root object. default: False
            filter (LottieObjectFilter): (optional) a predicate function which accepts a LottieObject and returns True / False to include / exclude the object
            include_classes (List[Type[LottieObject]]): (optional) a list of classes to include. default: include all lottie classes
            exclude_classes (List[Type[LottieObject]]): (optional) a list of classes to exclude. default: empty list

        Notes:
            At most one filter parameter can be set
        """
        filter = self._create_filter(**kwargs)
        children = [root] if include_self else self._get_children(root)
        self.__iter = self._iter(children=children, filter=filter)

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.__iter)

    @staticmethod
    def _iter(children: List[Type[LottieObject]], filter: LottieObjectFilter) -> LottieObjectIterator:
        """Returns a pre-order iterator for each child object

        Args:
            children (List[Type[LottieObject]]): a list of children objects
            filter (LottieObjectFilter): a filter function which accepts a lottie object, and returns True/False

        Returns:
            A LottieObject iterator
        """
        for child in children:
            if filter(child):
                yield child
            grandchildren = LottieIterator._get_children(child)
            for descendant in LottieIterator._iter(children=grandchildren, filter=filter):
                yield descendant

    @staticmethod
    def _create_filter(**kwargs) -> LottieObjectFilter:
        """Creates a lottie object filter function

        Args:
            filter (LottieObjectFilter): (optional) a predicate function which accepts a LottieObject and returns True / False to include / exclude the object
            include_classes (List[Type[LottieObject]]): (optional) a list of classes to include. default: include all lottie classes
            exclude_classes (List[Type[LottieObject]]): (optional) a list of classes to exclude. default: empty list

        Returns:
            A filter function which accepts a lottie object, and returns True/False
        """
        if sum(bool(kwargs.get(f)) for f in ('filter', 'include_classes', 'exclude_classes')) > 1:
            raise ValueError('Multiple filters provided - at most one filter parameter can be set')
        filters = []
        filters.append(lambda c: isinstance(c, LottieObject))
        if filter_ := kwargs.get('filter'):
            filters.append(filter_)
        if include_classes := kwargs.get('include_classes'):
            filters.append(lambda c: type(c) in include_classes)
        if exclude_classes := kwargs.get('exclude_classes'):
            filters.append(lambda c: type(c) not in exclude_classes)
        return lambda c: all(f(c) for f in filters)

    @staticmethod
    def _get_children(obj: LottieObject) -> List[LottieObject]:
        """Returns the dict-children of a LottieObject.
        Note: these are the dict-like children, i.e. those which are contained in the object

        Args:
            obj (LottieObject): parent object

        Returns:
            A list of child objects
        """
        children = []
        for value in obj.attributes.values():
            if isinstance(value, LottieObject):
                children.append(value)
            elif isinstance(value, List):
                children.extend(v for v in value if isinstance(v, LottieObject))
        return children

