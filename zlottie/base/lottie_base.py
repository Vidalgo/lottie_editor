from typing import Dict, ForwardRef, Type, Any

LottieBase = ForwardRef('LottieBase')


class LottieBase:
    def __init__(self, **kwargs):
        self._tag: str = kwargs.pop('tag', '')
        self._path: str = kwargs.pop('path', 'root')

    @property
    def tag(self):
        return self._tag

    @property
    def path(self):
        return self._path

    def load(self, raw: Any) -> None:
        raise NotImplementedError('Should be implemented in derived class')

    def dump(self) -> Any:
        raise NotImplementedError('Should be implemented in derived class')

    def clone(self):
        raise NotImplementedError('TODO')

    @classmethod
    def from_raw(cls, raw: Any) -> LottieBase:
        obj = cls()
        obj.load(raw=raw)
        return obj

    @classmethod
    def get_load_class(cls, raw: Dict) -> Type[LottieBase]:
        return cls

    def __repr__(self):
        return f"<{self.__class__.__name__} tag='{self._tag}'>"
