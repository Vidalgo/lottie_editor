from zlottie.base import LottieObject, LottieAttribute
from typing import List, Optional


class DummyLottieObjectWithoutInit(LottieObject):
    attr1: str = LottieAttribute(tag='a1', description='required string attribute')
    attr2: Optional[int] = LottieAttribute(tag='a2', description='optional int attribute')
    attr3: List[str] = LottieAttribute(tag='a3', description='required list attribute')


class DummyLottieObjectWithInit(LottieObject):
    attr1: str = LottieAttribute(tag='a1', description='required string attribute')
    attr2: Optional[int] = LottieAttribute(tag='a2')
    attr3: List[str] = LottieAttribute(tag='a3')

    def __init__(self, *args, **kwargs):
        self.x = kwargs.get('x', 1)


class DerivedDummyLottieObjectWithoutInit(DummyLottieObjectWithoutInit):
    # note that attr3 overrides both type and tag
    attr3: int = LottieAttribute(tag='x3', description='overrides attribute from baseclass')
    attr4: float = LottieAttribute(tag='a4')


class DerivedTwiceDummyLottieObjectWithoutInit(DerivedDummyLottieObjectWithoutInit):
    # note that attr3 overrides both type and tag
    attr5: bool = LottieAttribute(tag='a5')


class DummyLottieObject2(LottieObject):
    attr1: int = LottieAttribute(tag='a1', description='collides with DummyLottieObjectWithoutInit')
    attr6: bool = LottieAttribute(tag='a6')


class DummyLottieObjectMultipleInheritance(DummyLottieObjectWithoutInit, DummyLottieObject2):
    attr7: str = LottieAttribute(tag='a7')
