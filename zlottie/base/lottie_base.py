from typing import Dict, ForwardRef, Type, Any

LottieBase = ForwardRef('LottieBase')


class LottieBase:
    def __init__(self, **kwargs):
        self._tag: str = kwargs.pop('tag', '')

    @property
    def tag(self):
        return self._tag

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
