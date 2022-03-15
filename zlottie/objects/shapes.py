from zlottie.base import LottieObject, LottieAttribute
from zlottie.base import ShapeType, BlendMode, ShapeDirection
from zlottie.objects import VisualObject
from typing import Optional


class ShapeElement(VisualObject):
    hidden: Optional[bool] = LottieAttribute(tag='hd', description='Whether the shape is hidden')
    shape_type: ShapeType = LottieAttribute(tag='ty', description='Shape Type')
    blend_mode: Optional[BlendMode] = LottieAttribute(tag='bm', description='Blend Mode')
    property_index: Optional[int] = LottieAttribute(tag='cix', description='Index used in expressions')


class Shape(ShapeElement):
    direction: Optional[ShapeDirection] = LottieAttribute(tag='d', description='Direction the shape is drawn as, mostly relevant when using trim path')
