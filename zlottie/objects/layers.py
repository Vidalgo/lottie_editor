from zlottie.base import LottieAttribute
from zlottie.objects import VisualObject, RawObject, Transform
from zlottie.enums import BlendMode, LayerType, MatteMode
from typing import Optional, List, Dict, Type, Any

# TODO: implement the following
#Transform = RawObject
Mask = RawObject
Effect = RawObject
AudioSettings = RawObject
Value = RawObject
ShapeList = RawObject
TextAnimatorData = RawObject


class Layer(VisualObject):
    __classes_by_type: Dict[LayerType, Type] = {}

    three_dimensional: Optional[bool] = LottieAttribute(tag='ddd', default=0, description='Whether the layer is threedimensional')
    hidden: Optional[bool] = LottieAttribute(tag='hd', description='Whether the layer is hidden')
    type: LayerType = LottieAttribute(tag='ty', description='Layer Type')
    index: Optional[int] = LottieAttribute(tag='ind', description='Index')
    parent_index: Optional[int] = LottieAttribute(tag='parent', description='Must be the `ind` property of another layer')
    stretch: Optional[float] = LottieAttribute(tag='sr', default=1, description='Time Stretch')
    in_point: float = LottieAttribute(tag='ip', description='Frame when the layers becomes visible')
    out_point: float = LottieAttribute(tag='op', description='Frame when the layers becomes invisible')
    start_time: float = LottieAttribute(tag='st', description='Start Time')
    blend_mode: Optional[BlendMode] = LottieAttribute(tag='bm', default=0, description='Blend Mode')
    css_class: Optional[str] = LottieAttribute(tag='cl', description='CSS class used by the SVG renderer')
    id: Optional[str] = LottieAttribute(tag='ln', description='`id` attribute used by the SVG renderer')

    @staticmethod
    def register_layer_class(type_: LayerType, cls: Type):
        if type_ not in Layer.__classes_by_type:
            Layer.__classes_by_type[type_] = cls

    @classmethod
    def get_load_class(cls, raw: Any) -> Type['Layer']:
        layer_type = LayerType(raw['ty'])
        return Layer.__classes_by_type.get(layer_type, RawObject)


class VisualLayer(Layer):
    transform: Transform = LottieAttribute(tag='ks', description='Layer transform')
    auto_orient: Optional[bool] = LottieAttribute(tag='ao', default=0, description='Auto Orient')
    matte_mode: Optional[MatteMode] = LottieAttribute(tag='tt', description='Matte Mode')
    matte_target: Optional[int] = LottieAttribute(tag='td', description='Matte Target')
    has_masks: Optional[bool] = LottieAttribute(tag='hasMask', description='Whether the layer has masks applied')
    masks: Optional[Mask] = LottieAttribute(tag='masksProperties', description='Masks')
    effects: Optional[List[Effect]] = LottieAttribute(tag='ef', description='Effects')
    motion_blur: Optional[bool] = LottieAttribute(tag='mb', description='Whether motion blur is enabled for the layer')


class ShapeLayer(VisualLayer):
    shapes: ShapeList = LottieAttribute(tag='shapes', description='Shapes')


class PrecompositionLayer(VisualLayer):
    ref_id: str = LottieAttribute(tag='refId', description='ID of the precomp as specified in the assets')
    width: Optional[int] = LottieAttribute(tag='w', default=512, description='Width')
    height: Optional[int] = LottieAttribute(tag='h', default=512, description='Height')
    time_remapping: Optional[Value] = LottieAttribute(tag='tm', description='Time Remapping')


class NullLayer(VisualLayer):
    pass


class TextLayer(VisualLayer):
    data: TextAnimatorData = LottieAttribute(tag='t', description='Data')


class ImageLayer(VisualLayer):
    ref_id: str = LottieAttribute(tag='refId', description='ID of the image as specified in the assets')


class SolidColorLayer(VisualLayer):
    color: str = LottieAttribute(tag='sc', description='Color of the layer, unlike most other places, the color is a `#rrggbb` hex string')
    height: float = LottieAttribute(tag='sh', description='Height')
    width: float = LottieAttribute(tag='sw', description='Width')


class AudioLayer(Layer):
    audio_settings: AudioSettings = LottieAttribute(tag='au', description='Audio Settings')


# register classes
Layer.register_layer_class(LayerType.Shape, ShapeLayer)
Layer.register_layer_class(LayerType.Precomposition, PrecompositionLayer)
Layer.register_layer_class(LayerType.Null, NullLayer)
Layer.register_layer_class(LayerType.Text, TextLayer)
Layer.register_layer_class(LayerType.Image, ImageLayer)
Layer.register_layer_class(LayerType.SolidColor, SolidColorLayer)
Layer.register_layer_class(LayerType.Audio, AudioLayer)

__all__ = ['Layer', 'ShapeLayer', 'PrecompositionLayer', 'NullLayer', 'TextLayer', 'ImageLayer', 'SolidColorLayer', 'AudioLayer']
