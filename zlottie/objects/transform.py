from zlottie.base import RawLottieObject, LottieObject, LottieAttribute
from zlottie.types import Value#, MultiDimensional
from typing import Optional


# TODO: implement placeholders
Position = RawLottieObject
#Value = RawLottieObject
MultiDimensional = RawLottieObject


class Transform(LottieObject):
    anchor_point: Optional[Position] = LottieAttribute(tag='a', description='Anchor point: a position (relative to its parent) around which transformations are applied (ie: center for rotation / scale)')
    position: Optional[Position] = LottieAttribute(tag='p', description='Position / Translation')
    scale: Optional[MultiDimensional] = LottieAttribute(tag='s', description='Scale factor, `[100, 100]` for no scaling')
    rotation: Optional[Value] = LottieAttribute(tag='r', description='Rotation in degrees, clockwise')
    rotation_x: Optional[Value] = LottieAttribute(tag='rx', description='Split-rotation x-component')
    rotation_y: Optional[Value] = LottieAttribute(tag='ry', description='Split-rotation y-component')
    rotation_z: Optional[Value] = LottieAttribute(tag='rz', description='Split-rotation z-component')
    skew: Optional[Value] = LottieAttribute(tag='sk', description='Skew amount as an angle in degrees')
    skew_axis: Optional[Value] = LottieAttribute(tag='sa', description='Direction along which skew is applied, in degrees (`0` skews along the X axis, `90` along the Y axis)')
    opacity: Optional[Value] = LottieAttribute(tag='o', description='Opacity')
    orientation: Optional[MultiDimensional] = LottieAttribute(tag='or', description='Orientation')


class RepeaterTransform(Transform):
    start_opacity: Optional[Value] = LottieAttribute(tag='so', description='Start Opacity')
    end_opacity: Optional[Value] = LottieAttribute(tag='eo', description='End Opacity')
