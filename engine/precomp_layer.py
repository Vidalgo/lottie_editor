import copy
from engine.layer import Layer, Lottie_layer_type
from engine.animated_property import Animated_property


class Precomp_layer(Layer):
    def __init__(self, layer_id: int = 0, layer_name: str = 'unknown', ddd_layer: int = 0, layer_parent=None,
                 layer_transform=None, reference_id=None, width: float = 512, height: float = 512):
        Layer.__init__(self, layer_id, layer_name, ddd_layer, layer_parent, layer_transform, reference_id)
        self.type = Lottie_layer_type.Precomp
        self._time_remapping = None
        self.width = width
        self.height = height

    def analyze(self):
        Layer.analyze(self)
        if self.reference_id is None:
            raise TypeError("Error: precomp layer doesn't reference a precomposition")
        if self.vidalgo_id is None:
            raise TypeError("Error: layer doesn't have a vidalgo id")

    def load(self, layer: dict):
        Layer.load(self, layer)
        self.analyze()
        if 'tm' in layer:
            self._time_remapping = Animated_property()
            self._time_remapping.load(layer['tm'])

    def copy(self, layer: dict):
        Layer.copy(self, layer)

    @property
    def width(self):
        if 'w' in self.lottie_base:
            return self.lottie_base['w']
        else:
            return None

    @width.setter
    def width(self, width: float):
        self.lottie_base['w'] = width

    @property
    def height(self):
        if 'h' in self.lottie_base:
            return self.lottie_base['h']
        else:
            return None

    @height.setter
    def height(self, height: float):
        self.lottie_base['h'] = height

    @property
    def time_remapping(self):
        return self._time_remapping

    @time_remapping.setter
    def time_remapping(self, time_remapping: Animated_property):
        self._time_remapping = time_remapping
        if time_remapping is not None:
            self.lottie_base['tm'] = time_remapping.animated_property
