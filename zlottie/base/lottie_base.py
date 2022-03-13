from typing import Dict, ForwardRef, Type, Any

LottieBase = ForwardRef('LottieBase')


class LottieBase:
    def load(self, raw: Any) -> None:
        raise NotImplementedError('Should be implemented in derived class')

    def to_raw(self) -> Any:
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
