from typing import Dict, ForwardRef, Type

LottieBase = ForwardRef('LottieBase')


class LottieBase:
    def load(self, raw: Dict) -> None:
        raise NotImplementedError('Should be implemented in derived class')

    def to_dict(self) -> Dict:
        raise NotImplementedError('Should be implemented in derived class')

    def clone(self):
        raise NotImplementedError('TODO')

    @classmethod
    def from_dict(cls, raw: Dict) -> LottieBase:
        obj = cls()
        obj.load(raw=raw)
        return obj

    @classmethod
    def get_load_class(cls, raw: Dict) -> Type[LottieBase]:
        return cls
