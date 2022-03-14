from __future__ import annotations
import enum

from engine.vidalgo_lottie_base import Vidalgo_lottie_base
from engine.mask import Mask

from engine.transform import Transform


class Lottie_layer_type(enum.Enum):
    Precomp = 0
    Solid = 1
    Image = 2
    Null = 3
    Shape = 4
    Text = 5
    Audio = 6
    Pholder_video = 7
    Image_seq = 8
    Video = 9
    Pholder_stil = 10
    Guide = 11
    Adjustment = 12
    Camera = 13
    Light = 14
    Data = 15


class Blend_mode(enum.Enum):
    Normal = 0
    Multiply = 1
    Screen = 2
    Overlay = 3
    Darken = 4
    Lighten = 5
    Color_dodge = 6
    Color_burn = 7
    Hard_light = 8
    Soft_light = 9
    Difference = 10
    Exclusion = 11
    Hue = 12
    Saturation = 13
    Color = 14
    Luminosity = 15


class Matte_mode(enum.Enum):
    Normal = 0
    Alpha = 1
    Inverted_alpha = 2
    Luma = 3
    Inverted_luma = 4


class Layer(Vidalgo_lottie_base):
    def __init__(self, layer_id: int = 0, layer_name: str = 'unknown', ddd_layer: int = 0, layer_parent=None,
                 layer_transform=None, reference_id=None, out_point: int = 30, *args, **kwargs):
        super(Layer, self).__init__()
        self._transform = None
        self._masks = None
        self._effects = None
        self.id = layer_id
        self.name = layer_name
        self.ddd_layer = ddd_layer
        self.parent = layer_parent
        self.start_time = 0
        self.in_point = 0
        self.out_point = out_point
        self.reference_id = reference_id
        self.transform = layer_transform

    def analyze(self):
        super(Layer, self).analyze()
        '''if self.id is None:
            raise TypeError("Error: layer doesn't have an id")
        if self.name is None:
            raise TypeError("Error: layer doesn't have a name")'''
        '''if self.type is None:
            raise TypeError("Error: layer doesn't have a type")'''

    def load(self, layer: dict):
        self.lottie_base = layer
        if 'ks' in layer:
            self._transform = Transform()
            self._transform.load(layer['ks'])
        self.analyze()

    def copy(self, layer: Layer):
        super(Layer, self).copy(layer)
        layer.id = layer.id
        self.analyze()

    @property
    def layer(self):
        return self.lottie_base

    @layer.setter
    def layer(self, layer):
        self.lottie_base = layer
        self.analyze()

    @property
    def id(self):
        if 'ind' in self.lottie_base:
            return self.lottie_base['ind']
        else:
            return None

    @id.setter
    def id(self, layer_id: int):
        self.lottie_base['ind'] = layer_id

    @property
    def name(self):
        if 'nm' in self.lottie_base:
            return self.lottie_base['nm']
        else:
            return None

    @name.setter
    def name(self, layer_name: str):
        self.lottie_base['nm'] = layer_name

    @property
    def match_name(self):
        if 'mn' in self.lottie_base:
            return self.lottie_base['mn']
        else:
            return None

    @match_name.setter
    def match_name(self, match_name: str):
        self.lottie_base['mn'] = match_name

    @property
    def parent(self):
        if 'parent' in self.lottie_base:
            return self.lottie_base['parent']
        else:
            return None

    @parent.setter
    def parent(self, layer_parent: int):
        self.lottie_base['parent'] = layer_parent

    @property
    def transform(self):
        return self._transform

    @transform.setter
    def transform(self, layer_transform):
        if layer_transform is True:
            layer_transform = Transform()
        if layer_transform is None or layer_transform is False or type(layer_transform) is not Transform:
            self._transform = self.lottie_base['ks'] = None
            return
        self._transform = layer_transform
        self.lottie_base['ks'] = layer_transform.transform

    @property
    def reference_id(self):
        if 'refId' in self.lottie_base:
            return self.lottie_base['refId']
        else:
            return None

    @reference_id.setter
    def reference_id(self, new_transform):
        self.lottie_base['refId'] = new_transform

    @property
    def type(self):
        if 'ty' in self.lottie_base:
            return self.lottie_base['ty']
        else:
            return None

    @type.setter
    def type(self, layer_type: Lottie_layer_type):
        self.lottie_base['ty'] = layer_type.value

    @property
    def ddd_layer(self):
        if 'ddd' in self.lottie_base:
            return self.lottie_base['ddd']
        else:
            return None

    @ddd_layer.setter
    def ddd_layer(self, ddd_layer: int):
        if ddd_layer == 0 or ddd_layer == 1:
            self.lottie_base['ddd'] = ddd_layer

    def hide(self):
        self.lottie_base['hd'] = 1

    def reveal(self):
        self.lottie_base['hd'] = 0

    def hidden(self):
        if 'hd' in self.lottie_base and self.lottie_base['hd']:
            return True
        else:
            return False

    @staticmethod
    def get_type(layer: dict):
        if 'ty' in layer:
            return layer['ty']
        else:
            return None

    @property
    def time_stretch(self):
        if 'sr' in self.lottie_base:
            return self.lottie_base['sr']
        else:
            return None

    @time_stretch.setter
    def time_stretch(self, time_stretch: float):
        self.lottie_base['sr'] = time_stretch

    @property
    def in_point(self):
        if 'ip' in self.lottie_base:
            return self.lottie_base['ip']
        else:
            return None

    @in_point.setter
    def in_point(self, in_point: float):
        self.lottie_base['ip'] = in_point

    @property
    def out_point(self):
        if 'op' in self.lottie_base:
            return self.lottie_base['op']
        else:
            return None

    @out_point.setter
    def out_point(self, out_point: float):
        self.lottie_base['op'] = out_point

    @property
    def start_time(self):
        if 'st' in self.lottie_base:
            return self.lottie_base['st']
        else:
            return None

    @start_time.setter
    def start_time(self, start_time: float):
        self.lottie_base['st'] = start_time

    @property
    def blend_mode(self):
        if 'bm' in self.lottie_base:
            return self.lottie_base['bm']
        else:
            return None

    @blend_mode.setter
    def blend_mode(self, blend_mode: Blend_mode):
        self.lottie_base['bm'] = blend_mode.value

    @property
    def layer_class(self):
        if 'cl' in self.lottie_base:
            return self.lottie_base['cl']
        else:
            return None

    @layer_class.setter
    def layer_class(self, layer_class: str):
        self.lottie_base['cl'] = layer_class

    @property
    def layer_html_id(self):
        if 'ln' in self.lottie_base:
            return self.lottie_base['ln']
        else:
            return None

    @layer_html_id.setter
    def layer_html_id(self, layer_html_id: str):
        self.lottie_base['ln'] = layer_html_id

    @property
    def has_mask(self):
        if 'hasMask' in self.lottie_base:
            return self.lottie_base['hasMask']
        else:
            return None

    @has_mask.setter
    def has_mask(self, has_mask: bool):
        self.lottie_base['hasMask'] = has_mask

    @property
    def auto_orient(self):
        if 'ao' in self.lottie_base:
            return self.lottie_base['ao']
        else:
            return None

    @auto_orient.setter
    def auto_orient(self, auto_orient: int):
        if auto_orient == 0 or auto_orient == 1:
            self.lottie_base['ao'] = auto_orient

    @property
    def matte_mode(self):
        if 'tt' in self.lottie_base:
            return self.lottie_base['tt']
        else:
            return None

    @matte_mode.setter
    def matte_mode(self, matte_mode: Matte_mode):
        self.lottie_base['tt'] = matte_mode.value

    @property
    def matte_target(self):
        if 'td' in self.lottie_base:
            return self.lottie_base['td']
        else:
            return None

    @matte_target.setter
    def matte_target(self, matte_target: int):
        self.lottie_base['td'] = matte_target

    @property
    def masks_properties(self):
        if 'masksProperties' in self.lottie_base:
            return self.lottie_base['masksProperties']
        else:
            return None

    @masks_properties.setter
    def masks_properties(self, masks_properties: None):
        if masks_properties is not None and type(masks_properties) is list(Mask):
            self.lottie_base['masksProperties'] = masks_properties
        else:
            self.lottie_base['masksProperties'] = None

    @property
    def effects(self):
        if 'ef' in self.lottie_base:
            return self.lottie_base['ef']
        else:
            return None

    @effects.setter
    def effects(self, effects: None):
        if effects is not None and type(effects) is list(Effect):
            self.lottie_base['ef'] = effects
        else:
            self.lottie_base['ef'] = None

    @property
    def motion_blur(self):
        if 'mb' in self.lottie_base:
            return self.lottie_base['mb']
        else:
            return None

    @motion_blur.setter
    def motion_blur(self, motion_blur: bool):
        self.lottie_base['mb'] = motion_blur


def find_layer(layers: list[Layer], layer_id: int = None, layer_name: str = None):
    if layers is not None:
        if layer_id is not None:
            for index, layer in enumerate(layers):
                if layer.id == layer_id:
                    return index
        elif layer_name is not None:
            for index, layer in enumerate(layers):
                if layer.name is not None and layer.name == layer_name:
                    return index
    return None


def add_layer(layers: list[Layer], new_layer: Layer, order='last', layer_id: int = None, layer_name: str = None):
    if order == 'first':
        layers.insert(0, new_layer)
        return 0
    elif order == 'last':
        layers.append(new_layer)
        return len(layers)
    else:
        layer_index = find_layer(layers, layer_id, layer_name)
        if layer_index is not None:
            if order == 'before':
                layers.insert(layer_index, new_layer)
                return layer_index
            elif order == 'after':
                layers.insert(layer_index + 1, new_layer)
                return layer_index + 1
    return None


def replace_layer(layers: list[Layer], new_layer: Layer, layer_id: int = None, layer_name: str = None):
    layer_index = find_layer(layers, layer_id, layer_name)
    if layer_index is not None:
        layer_id = layers[layer_index].id
        layers[layer_index] = new_layer
        new_layer.id = layer_id
        return layer_index
    return None


def delete_layer(layers: list[Layer], layer_id: int, layer_name: str = None):
    layer_index = find_layer(layers, layer_id, layer_name)
    if layer_index is not None:
        layers.remove(layers[layer_index])
        return layer_index
    return None


def update_ref_id(layers: list[Layer], layer_type: Lottie_layer_type, ref_id: str, updated_ref_id: str):
    for layer in layers:
        if layer.reference_id is not None and layer.type == layer_type.value and layer.reference_id == ref_id:
            layer.reference_id = updated_ref_id
