from zlottie.base import LottieObject, LottieAttribute
from zlottie.objects import RawObject
from zlottie.types import Value#, MultiDimensional
from typing import Optional


# TODO: implement placeholders
Position = RawObject
#Value = RawObject
MultiDimensional = RawObject


class Transform(LottieObject):
    anchor_point: Optional[Position] = LottieAttribute(tag='a', description='Anchor point: a position (relative to its parent) around which transformations are applied (ie: center for rotation / scale)')
    position: Optional[Position] = LottieAttribute(tag='p', description='Position / Translation')
    scale: Optional[MultiDimensional] = LottieAttribute(tag='s', description='Scale factor, `[100, 100]` for no scaling')
    rotation: Optional[Value] = LottieAttribute(tag='r', description='Rotation in degrees, clockwise')
    skew: Optional[Value] = LottieAttribute(tag='sk', description='Skew amount as an angle in degrees')
    skew_axis: Optional[Value] = LottieAttribute(tag='sa', description='Direction along which skew is applied, in degrees (`0` skews along the X axis, `90` along the Y axis)')
    opacity: Optional[Value] = LottieAttribute(tag='o', description='Opacity')
