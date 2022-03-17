from zlottie.base import RawLottieObject, LottieObject, LottieAttribute
from zlottie.enums import *
from zlottie.objects import VisualObject, Transform, RepeaterTransform
from zlottie.types import Value, ColorValue, MultiDimensional, AnimatedProperty
from typing import Optional, List, Dict, Type, Any

# TODO: implement
Position = RawLottieObject
ShapeProperty = AnimatedProperty


# Base classes (see zlottie.enums.ShapeType)
class ShapeBase(LottieObject):
    __classes_by_type: Dict[ShapeType, Type] = {}

    shape_type: ShapeType = LottieAttribute(tag='ty', description='Shape Type')
    id: Optional[str] = LottieAttribute(tag='ln', description='`id` attribute used by the SVG renderer')
    name: Optional[str] = LottieAttribute(tag='nm', description='Name, as seen from editors and the like')
    match_name: Optional[str] = LottieAttribute(tag='mn', description='Match name, used in expression')
    class_name: Optional[str] = LottieAttribute(tag='cl', description='CSS class used by the SVG renderer')
    is_hidden: Optional[bool] = LottieAttribute(tag='hd', description='Whether the shape is hidden')

    @staticmethod
    def register_shape_class(type_: ShapeType, cls: Type):
        if type_ not in ShapeBase.__classes_by_type:
            ShapeBase.__classes_by_type[type_] = cls

    @classmethod
    def get_load_class(cls, raw: Any) -> Type['Layer']:
        type_ = ShapeType(raw['ty'])
        return ShapeBase.__classes_by_type.get(type_, RawLottieObject)


# Shape
class BasicShape(ShapeBase):
    direction: Optional[ShapeDirection] = LottieAttribute(tag='d', default=ShapeDirection.Normal, description='Direction the shape is drawn as, mostly relevant when using trim path')


class Rectangle(BasicShape):
    position: Position = LottieAttribute(tag='p', description='Center of the rectangle')
    size: MultiDimensional = LottieAttribute(tag='s', description='Size')
    roundness: Value = LottieAttribute(tag='r', description='Rounded')


class Ellipse(BasicShape):
    position: Position = LottieAttribute(tag='p', description='Position')
    size: MultiDimensional = LottieAttribute(tag='s', description='Size')


class PolyStar(BasicShape):
    star_type: Optional[StarType] = LottieAttribute(tag='sy', default=StarType.Star, description='Star type, `1` for Star, `2` for Polygon')
    position: Position = LottieAttribute(tag='p', description='Position')
    outer_radius: Value = LottieAttribute(tag='or', description='Outer Radius')
    outer_roundness: Value = LottieAttribute(tag='os', description='Outer Roundness as a percentage')
    rotation: Value = LottieAttribute(tag='r', description='Rotation, clockwise in degrees')
    points: Value = LottieAttribute(tag='pt', description='Points')
    # additional properties when star_type == StarType.Star
    inner_radius: Optional[Value] = LottieAttribute(tag='ir', description='Outer Radius')
    inner_roundness: Optional[Value] = LottieAttribute(tag='is', description='Outer Roundness as a percentage')


class Path(BasicShape):
    vertices: ShapeProperty = LottieAttribute(tag='ks', description='Path vertices')
    item_index: Optional[int] = LottieAttribute(tag='ind', description='Item index')
    shape_index: Optional[int] = LottieAttribute(tag='ix', description='Shape Index')


# Style
class StyleShape(ShapeBase):
    pass


class FillShape(StyleShape):
    opacity: Value = LottieAttribute(tag='o', description='Opacity')
    color: ColorValue = LottieAttribute(tag='c', description='Color')
    blend_mode: Optional[BlendMode] = LottieAttribute(tag='bm', description='Blend Mode')
    fill_rule: Optional[FillRule] = LottieAttribute(tag='r', description='Fill Rule')


class GradientColors(LottieObject):
    colors: MultiDimensional = LottieAttribute(tag='k', description='Colors')
    color_count: int = LottieAttribute(tag='p', description='Number of colors in `k`')


class Gradient(LottieObject):
    start_point: MultiDimensional = LottieAttribute(tag='s', description='Start Point')
    end_point: MultiDimensional = LottieAttribute(tag='e', description='End Point')
    gradient_type: Optional[GradientType] = LottieAttribute(tag='t', default=GradientType.Linear, description='Gradient Type')
    highlight_length: Optional[Value] = LottieAttribute(tag='h', description='Highlight Length')
    highlight_angle: Optional[Value] = LottieAttribute(tag='a', description='Highlight Angle')
    colors: GradientColors = LottieAttribute(tag='g', description='Colors')


class StrokeShape(ShapeBase):
    opacity: Value = LottieAttribute(tag='o', description='Opacity')
    color: MultiDimensional = LottieAttribute(tag='c', description='Color')
    width: Value = LottieAttribute(tag='w', description='Width')
    line_cap: Optional[LineCap] = LottieAttribute(tag='lc', default=LineCap.Round, description='Line Cap')
    line_join: Optional[LineJoin] = LottieAttribute(tag='lj', default=LineJoin.Round, description='Line Join')
    miter_limit: Optional[float] = LottieAttribute(tag='ml', default=0.0, description='Miter Limit')
    miter_limit_2: Optional[Value] = LottieAttribute(tag='ml2', description='Animatable alternative to ml')
    blend_mode: Optional[BlendMode] = LottieAttribute(tag='bm', description='Blend Mode')


class GradientFillShape(ShapeBase):
    start_point: MultiDimensional = LottieAttribute(tag='s', description='Start Point')
    end_point: MultiDimensional = LottieAttribute(tag='e', description='End Point')
    gradient_type: GradientType = LottieAttribute(tag='t', default=GradientType.Linear, description='Gradient Type')
    opacity: Value = LottieAttribute(tag='o', description='Opacity')
    colors: GradientColors = LottieAttribute(tag='g', description='Colors')
    fill_rule: Optional[FillRule] = LottieAttribute(tag='r', default=FillRule.EvenOdd, description='Fill Rule')
    blend_mode: Optional[BlendMode] = LottieAttribute(tag='bm', default=BlendMode.Normal, description='Blend Mode')
    # additional properties when gradient_type == GradientType.Radial
    highlight_length: Optional[Value] = LottieAttribute(tag='h', description='Highlight Length')
    highlight_angle: Optional[Value] = LottieAttribute(tag='a', description='Highlight Angle')


class GradientStrokeShape(ShapeBase):
    opacity: Value = LottieAttribute(tag='o', description='Opacity')
    blend_mode: Optional[BlendMode] = LottieAttribute(tag='bm', description='Blend Mode')
    # Gradient
    start_point: MultiDimensional = LottieAttribute(tag='s', description='Start Point')
    end_point: MultiDimensional = LottieAttribute(tag='e', description='End Point')
    gradient_type: Optional[GradientType] = LottieAttribute(tag='t', default=GradientType.Linear, description='Gradient Type')
    colors: GradientColors = LottieAttribute(tag='g', description='Colors')
    # additional properties when gradient_type == GradientType.Radial
    highlight_length: Optional[Value] = LottieAttribute(tag='h', description='Highlight Length')
    highlight_angle: Optional[Value] = LottieAttribute(tag='a', description='Highlight Angle')
    # Stroke
    line_cap: Optional[LineCap] = LottieAttribute(tag='lc', default=LineCap.Round, description='Line Cap')
    line_join: Optional[LineJoin] = LottieAttribute(tag='lj', default=LineJoin.Round, description='Line Join')
    miter_limit: Optional[float] = LottieAttribute(tag='ml', default=0.0, description='Miter Limit')
    miter_limit_2: Optional[Value] = LottieAttribute(tag='ml2', description='Animatable alternative to ml')
    width: Value = LottieAttribute(tag='w', description='Width')


# Group
class GroupShape(ShapeBase):
    blend_mode: Optional[BlendMode] = LottieAttribute(tag='bm', description='Blend Mode')
    shapes: Optional[List[ShapeBase]] = LottieAttribute(tag='it', description='Shapes')
    num_properties: Optional[float] = LottieAttribute(tag='np', description='Number Of Properties')
    property_index: Optional[int] = LottieAttribute(tag='ix', description='Shape Index')
    content_property_index: Optional[int] = LottieAttribute(tag='cix', description='Index used in expressions')


# Transform shape
class TransformShape(ShapeBase, Transform):
    pass


# Modifiers
class ModifierShape(ShapeBase):
    pass


class RepeaterShape(ModifierShape):
    copies: Value = LottieAttribute(tag='c', description='Copies')
    offset: Optional[Value] = LottieAttribute(tag='o', description='Offset')
    composition: Optional[Composite] = LottieAttribute(tag='m', default=Composite.Above, description='Composition')
    transform: RepeaterTransform = LottieAttribute(tag='tr', description='Transform')


class TrimShape(ModifierShape):
    trim_start: Value = LottieAttribute(tag='s', description='Start')
    trim_offset: Value = LottieAttribute(tag='o', description='Offset')
    trim_end: Value = LottieAttribute(tag='e', description='End')
    blend_mode: Optional[BlendMode] = LottieAttribute(tag='bm', default=BlendMode.Normal, description='Blend Mode')
    multiple: Optional[TrimMultipleShapes] = LottieAttribute(tag='m', default=TrimMultipleShapes.Individually, description='Multiple')


class RoundedCornersShape(ModifierShape):
    radius: Value = LottieAttribute(tag='r', description='Radius')


class PuckerBloatShape(ShapeBase):
    amount: Optional[Value] = LottieAttribute(tag='a', description='Amount as a percentage')


class MergeShape(ShapeBase):
    merge_mode: Optional[float] = LottieAttribute(tag='mm', default=1.0, description='Merge Mode')


class TwistShape(ShapeBase):
    angle: Optional[Value] = LottieAttribute(tag='a', description='Angle')
    center: Optional[MultiDimensional] = LottieAttribute(tag='c', description='Center')


class OffsetPathShape(ShapeBase):
    amount: Optional[Value] = LottieAttribute(tag='a', description='Amount')
    line_join: Optional[LineJoin] = LottieAttribute(tag='lj', default=LineJoin.Round, description='Line Join')
    miter_limit: Optional[Value] = LottieAttribute(tag='ml', description='Miter Limit')


class ZigZagShape(ShapeBase):
    roundness: Optional[Value] = LottieAttribute(tag='r', description='Radius to maked it a smoother curve')
    size: Optional[Value] = LottieAttribute(tag='s', description='Distance between peaks and troughs')
    points: Optional[Value] = LottieAttribute(tag='pt', description='Number of ridges')


# register classes
ShapeBase.register_shape_class(ShapeType.Rectangle, Rectangle)
ShapeBase.register_shape_class(ShapeType.Ellipse, Ellipse)
ShapeBase.register_shape_class(ShapeType.PolyStar, PolyStar)
ShapeBase.register_shape_class(ShapeType.Path, Path)
ShapeBase.register_shape_class(ShapeType.Fill, FillShape)
ShapeBase.register_shape_class(ShapeType.Stroke, StrokeShape)
ShapeBase.register_shape_class(ShapeType.GradientFill, GradientFillShape)
ShapeBase.register_shape_class(ShapeType.GradientStroke, GradientStrokeShape)
ShapeBase.register_shape_class(ShapeType.Group, GroupShape)
ShapeBase.register_shape_class(ShapeType.Transform, TransformShape)
ShapeBase.register_shape_class(ShapeType.Repeater, RepeaterShape)
ShapeBase.register_shape_class(ShapeType.Trim, TrimShape)
ShapeBase.register_shape_class(ShapeType.RoundedCorners, RoundedCornersShape)
ShapeBase.register_shape_class(ShapeType.PuckerBloat, PuckerBloatShape)
ShapeBase.register_shape_class(ShapeType.Merge, MergeShape)
ShapeBase.register_shape_class(ShapeType.Twist, TwistShape)
ShapeBase.register_shape_class(ShapeType.OffsetPath, OffsetPathShape)
ShapeBase.register_shape_class(ShapeType.ZigZag, ZigZagShape)


__all__ = [
    'ShapeBase', 'BasicShape', 'Rectangle', 'Ellipse', 'PolyStar', 'Path', 'FillShape', 'GradientColors', 'Gradient',
    'StrokeShape', 'GradientFillShape', 'GradientStrokeShape', 'GroupShape', 'TransformShape', 'ModifierShape', 'RepeaterShape',
    'TrimShape', 'RoundedCornersShape', 'PuckerBloatShape', 'MergeShape', 'TwistShape', 'OffsetPathShape', 'ZigZagShape']
