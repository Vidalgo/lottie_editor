from zlottie.base import LottieObject, LottieAttribute
from zlottie.objects import RawObject
from typing import Optional, Union, Dict, Any, List
from numbers import Number


# TODO: implement Keyframe
Keyframe = RawObject

RawValueOrKeyframes = Union[Number, List[Number], List[Keyframe]]


class ValueOrKeyframes(LottieObject):
    _value: Any = None
    _keyframes: List[Keyframe] = None
    _is_value: bool = None
    _is_keyframes: bool = None

    def load(self, raw: RawValueOrKeyframes) -> None:
        if isinstance(raw, List) and isinstance(raw[0], dict):
            self._keyframes = [Keyframe(d) for d in raw]
        else:
            self._value = raw

    def to_dict(self) -> RawValueOrKeyframes:
        if self.is_value is not None:
            return self._value
        elif self.is_keyframes is not None:
            return [k.to_dict() for k in self._keyframes]
        else:
            return None

    @property
    def value(self) -> Number:
        return self._value

    @property
    def keyframes(self) -> List[Keyframe]:
        return self._keyframes

    @property
    def is_value(self) -> bool:
        return self._value is not None

    @property
    def is_keyframes(self) -> bool:
        return self._keyframes is not None


class AnimatedProperty(LottieObject):
    animated: bool = LottieAttribute(tag='a', description='Whether the property is animated')
    _value: ValueOrKeyframes = LottieAttribute(tag='k', description='Value or keyframes, this changes based on the value of a')
    property_index: Optional[int] = LottieAttribute(tag='ix', description='Property Index')
    expression: Optional[str] = LottieAttribute(tag='x', description='Expression')

    @property
    def value(self) -> Number:
        return self._value.value

    @property
    def keyframes(self) -> List[Keyframe]:
        return self._value.keyframes

    @property
    def is_value(self) -> bool:
        return self._value.is_value

    @property
    def is_keyframes(self) -> bool:
        return self._value.is_keyframes


class Value(AnimatedProperty):
    pass


class ColorValue(AnimatedProperty):
    pass


class MultiDimensional(AnimatedProperty):
    pass
