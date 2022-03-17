from zlottie.base import RawLottieObject, LottieObject, LottieAttribute
from zlottie.enums import *
from zlottie.objects import VisualObject, Transform, RepeaterTransform
from zlottie.types import Value, ColorValue, MultiDimensional, AnimatedProperty
from typing import Optional, List, Dict, Type, Any

# TODO: implement
Position = RawLottieObject
ShapeProperty = AnimatedProperty


# Base classes (see zlottie.enums.ShapeType)
class ShapeElement(VisualObject):
    __classes_by_type: Dict[ShapeType, Type] = {}

    hidden: Optional[bool] = LottieAttribute(tag='hd', description='Whether the shape is hidden')
    shape_type: ShapeType = LottieAttribute(tag='ty', description='Shape Type')
    blend_mode: Optional[BlendMode] = LottieAttribute(tag='bm', description='Blend Mode')
    property_index: Optional[int] = LottieAttribute(tag='cix', description='Index used in expressions')

    @staticmethod
    def register_shape_class(type_: LayerType, cls: Type):
        if type_ not in ShapeElement.__classes_by_type:
            ShapeElement.__classes_by_type[type_] = cls

    @classmethod
    def get_load_class(cls, raw: Any) -> Type['Layer']:
        type_ = ShapeType(raw['ty'])
        return ShapeElement.__classes_by_type.get(type_, RawLottieObject)


# Shape
class Shape(ShapeElement):
    direction: Optional[ShapeDirection] = LottieAttribute(tag='d', description='Direction the shape is drawn as, mostly relevant when using trim path')


class Rectangle(Shape):
    position: Position = LottieAttribute(tag='p', description='Center of the rectangle')
    size: MultiDimensional = LottieAttribute(tag='s', description='Size')
    rounded: Value = LottieAttribute(tag='r', description='Rounded')


class Ellipse(Shape):
    position: Position = LottieAttribute(tag='p', description='Position')
    size: MultiDimensional = LottieAttribute(tag='s', description='Size')


class PolyStar(Shape):
    position: Position = LottieAttribute(tag='p', description='Position')
    outer_radius: Value = LottieAttribute(tag='or_', description='Outer Radius')
    outer_roundness: Value = LottieAttribute(tag='os', description='Outer Roundness as a percentage')
    rotation: Value = LottieAttribute(tag='r', description='Rotation, clockwise in degrees')
    points: Value = LottieAttribute(tag='pt', description='Points')
    star_type: Optional[StarType] = LottieAttribute(tag='sy', default=StarType.Star, description='Star type, `1` for Star, `2` for Polygon')


class Path(Shape):
    shape: ShapeProperty = LottieAttribute(tag='ks', description='Shape')
    index: Optional[int] = LottieAttribute(tag='ind', description='Index')


class Fill(ShapeElement):
    opacity: Value = LottieAttribute(tag='o', description='Opacity')
    color: ColorValue = LottieAttribute(tag='c', description='Color')
    fill_rule: Optional[FillRule] = LottieAttribute(tag='r', description='Fill Rule')


# Style
class GradientColors(LottieObject):
    colors: MultiDimensional = LottieAttribute(tag='k', description='Colors')
    count: int = LottieAttribute(tag='p', description='Number of colors in `k`')


class Gradient(LottieObject):
    start_point: MultiDimensional = LottieAttribute(tag='s', description='Start Point')
    end_point: MultiDimensional = LottieAttribute(tag='e', description='End Point')
    gradient_type: Optional[GradientType] = LottieAttribute(tag='t', default=GradientType.Linear, description='Gradient Type')
    highlight_length: Optional[Value] = LottieAttribute(tag='h', description='Highlight Length')
    highlight_angle: Optional[Value] = LottieAttribute(tag='a', description='Highlight Angle')
    colors: GradientColors = LottieAttribute(tag='g', description='Colors')


class BaseStroke(LottieObject):
    line_cap: Optional[LineCap] = LottieAttribute(tag='lc', default=LineCap.Round, description='Line Cap')
    line_join: Optional[LineJoin] = LottieAttribute(tag='lj', default=LineJoin.Round, description='Line Join')
    miter_limit: Optional[float] = LottieAttribute(tag='ml', default=0.0, description='Miter Limit')
    opacity: Value = LottieAttribute(tag='o', description='Opacity')
    width: Value = LottieAttribute(tag='w', description='Width')
    dashes: Optional[List[StrokeDashType]] = LottieAttribute(tag='d', description='Dashes')


class Stroke(ShapeElement, BaseStroke):
    color: MultiDimensional = LottieAttribute(tag='c', description='Color')


class GradientFill(ShapeElement, Gradient):
    opacity: Value = LottieAttribute(tag='o', description='Opacity')
    fill_rule: Optional[FillRule] = LottieAttribute(tag='r', description='Fill Rule')


class GradientStroke(ShapeElement, BaseStroke, Gradient):
    pass


# Group
class Group(ShapeElement):
    number_of_properties: Optional[float] = LottieAttribute(tag='np', description='Number Of Properties')
    shapes: Optional[List[ShapeElement]] = LottieAttribute(tag='it', description='Shapes')


class TransformShape(ShapeElement, Transform):
    pass


# Modifiers
class Modifier(ShapeElement):
    pass


class Repeater(Modifier):
    copies: Value = LottieAttribute(tag='c', description='Copies')
    offset: Optional[Value] = LottieAttribute(tag='o', description='Offset')
    composite: Optional[Composite] = LottieAttribute(tag='m', default=Composite.Above, description='Composite')
    transform: RepeaterTransform = LottieAttribute(tag='tr', description='Transform')


class Trim(Modifier):
    start: Value = LottieAttribute(tag='s', description='Start')
    end: Value = LottieAttribute(tag='e', description='End')
    offset: Value = LottieAttribute(tag='o', description='Offset')
    multiple: Optional[TrimMultipleShapes] = LottieAttribute(tag='m', description='Multiple')


class RoundedCorners(Modifier):
    radius: Value = LottieAttribute(tag='r', description='Radius')


class PuckerBloat(ShapeElement):
    amount: Optional[Value] = LottieAttribute(tag='a', description='Amount as a percentage')


class Merge(ShapeElement):
    merge_mode: Optional[float] = LottieAttribute(tag='mm', default=1.0, description='Merge Mode')


class Twist(ShapeElement):
    angle: Optional[Value] = LottieAttribute(tag='a', description='Angle')
    center: Optional[MultiDimensional] = LottieAttribute(tag='c', description='Center')


class OffsetPath(ShapeElement):
    amount: Optional[Value] = LottieAttribute(tag='a', description='Amount')
    line_join: Optional[LineJoin] = LottieAttribute(tag='lj', default=LineJoin.Round, description='Line Join')
    miter_limit: Optional[Value] = LottieAttribute(tag='ml', description='Miter Limit')


class ZigZag(ShapeElement):
    roundness: Optional[Value] = LottieAttribute(tag='r', description='Radius to maked it a smoother curve')
    size: Optional[Value] = LottieAttribute(tag='s', description='Distance between peaks and troughs')
    points: Optional[Value] = LottieAttribute(tag='pt', description='Number of ridges')


# register classes
ShapeElement.register_shape_class(ShapeType.Rectangle, Rectangle)
ShapeElement.register_shape_class(ShapeType.Ellipse, Ellipse)
ShapeElement.register_shape_class(ShapeType.PolyStar, PolyStar)
ShapeElement.register_shape_class(ShapeType.Path, Path)
ShapeElement.register_shape_class(ShapeType.Fill, Fill)
ShapeElement.register_shape_class(ShapeType.Stroke, Stroke)
ShapeElement.register_shape_class(ShapeType.GradientFill, GradientFill)
ShapeElement.register_shape_class(ShapeType.GradientStroke, GradientStroke)
ShapeElement.register_shape_class(ShapeType.Group, Group)
ShapeElement.register_shape_class(ShapeType.Transform, TransformShape)
ShapeElement.register_shape_class(ShapeType.Repeater, Repeater)
ShapeElement.register_shape_class(ShapeType.Trim, Trim)
ShapeElement.register_shape_class(ShapeType.RoundedCorners, RoundedCorners)
ShapeElement.register_shape_class(ShapeType.PuckerBloat, PuckerBloat)
ShapeElement.register_shape_class(ShapeType.Merge, Merge)
ShapeElement.register_shape_class(ShapeType.Twist, Twist)
ShapeElement.register_shape_class(ShapeType.OffsetPath, OffsetPath)
ShapeElement.register_shape_class(ShapeType.ZigZag, ZigZag)

__all__ = [
    'ShapeElement', 'Shape', 'Rectangle', 'Ellipse', 'PolyStar', 'Path', 'Fill', 'GradientColors', 'Gradient',
    'BaseStroke', 'Stroke', 'GradientFill', 'GradientStroke', 'Group', 'TransformShape', 'Modifier', 'Repeater',
    'Trim', 'RoundedCorners', 'PuckerBloat', 'Merge', 'Twist', 'OffsetPath', 'ZigZag']
