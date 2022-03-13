from zlottie.base import LottieBase, LottieObject, LottieAttribute
from zlottie.objects import RawObject
from zlottie.types import Vector
from typing import Optional, Union, Dict, Any, List
from numbers import Number


# TODO: implement Keyframe
Keyframe = RawObject
ValueType = Union[Number, Vector, List[Keyframe]]


class AnimatedProperty(LottieObject):
    is_animated: bool = LottieAttribute(tag='a', description='Whether the property is animated')
    value: ValueType = LottieAttribute(tag='k', autoload=False, description='Value or keyframes, this changes based on the value of a')
    property_index: Optional[int] = LottieAttribute(tag='ix', description='Property Index')
    expression: Optional[str] = LottieAttribute(tag='x', description='Expression')

    def load(self, raw: Dict) -> None:
        super().load(raw=raw)
        if self.is_animated:
            self.value = [Keyframe(d) for d in raw['k']]
        else:
            self.value = raw['k']


class Value(AnimatedProperty):
    pass


class ColorValue(AnimatedProperty):
    pass


class MultiDimensional(AnimatedProperty):
    pass
