from enum import Enum


class LayerType(Enum):
    Precomposition = 0
    SolidColor = 1
    Image = 2
    Null = 3
    Shape = 4
    Text = 5
    Audio = 6
    Invalid = -1

    @classmethod
    def _missing_(cls, value):
        return LayerType.Invalid


class BlendMode(Enum):
    Normal = 0
    Multiply = 1
    Screen = 2
    Overlay = 3
    Darken = 4
    Lighten = 5
    ColorDodge = 6
    ColorBurn = 7
    HardLight = 8
    SoftLight = 9
    Difference = 10
    Exclusion = 11
    Hue = 12
    Saturation = 13
    Color = 14
    Luminosity = 15


class MatteMode(Enum):
    Normal = 0
    Alpha = 1
    InvertedAlpha = 2
    Luma = 3
    InvertedLuma = 4


class ShapeType(Enum):
    Rectangle = 'rc'
    Ellipse = 'el'
    PolyStar = 'sr'
    Path = 'sh'
    Fill = 'fl'
    Stroke = 'st'
    GradientFill = 'gf'
    GradientStroke = 'gs'
    Group = 'gr'
    Transform = 'tr'
    Repeater = 'rp'
    Trim = 'tm'
    RoundedCorners = 'rd'
    PuckerBloat = 'pb'
    Merge = 'mm'
    Twist = 'tw'
    OffsetPath = 'op'
    ZigZag = 'zz'


class ShapeDirection(Enum):
    Normal = 1      # Usually clockwise
    Reversed = 3    # Usually counter clockwise

    @classmethod
    def _missing_(cls, value):
        return ShapeDirection.Normal


class StarType(Enum):
    Star = 1
    Polygon = 2


class FillRule(Enum):
    NonZero = 1
    EvenOdd = 2


class LineJoin(Enum):
    Miter = 1
    Round = 2
    Bevel = 3


class LineCap(Enum):
    Butt = 1
    Round = 2
    Square = 3


class StrokeDashType(Enum):
    Dash = 'd'
    Gap = 'g'
    Offset = 'o'


class GradientType(Enum):
    Linear = 1
    Radial = 2


class Composite(Enum):
    Above = 1
    Below = 2


class TrimMultipleShapes(Enum):
    Individually = 1
    Simultaneously = 2
