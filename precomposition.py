from vidalgo_lottie_base import Vidalgo_lottie_base
from layer import Layer, Lottie_layer_type, find_layer, add_layer, delete_layer, replace_layer
from text_layer import Text_layer


class Precomposition(Vidalgo_lottie_base):
    def __init__(self, precomp_id: str = None, precomp_name: str = None, framerate: float = 30):
        super(Precomposition, self).__init__()
        self._main_layers_index = 0
        self._layers: list[Layer] = []
        self.id = precomp_id
        self.name = precomp_name
        self.framerate = framerate
        self.layers = []

    def load(self, precomp: dict):
        def _load_layer(layer: dict):
            layer_type = '{0}_layer'.format(Lottie_layer_type(Layer.get_type(layer)).name)
            new_layer = globals()[layer_type]() if layer_type in globals() else Layer()
            new_layer.load(layer)
            return new_layer

        self.lottie_base = precomp
        self.analyze()
        self._layers = [] if 'layers' not in precomp else [_load_layer(layer) for layer in self.lottie_base['layers']]

    def copy(self, animation: dict):
        super(Precomposition, self).copy(animation)
        self.analyze()

    def analyze(self):
        super(Precomposition, self).analyze()
        if self.id is None:
            raise TypeError("Error: precomposition id is missing")

    @property
    def precomp(self):
        return self.lottie_base

    @precomp.setter
    def precomp(self, precomp: dict):
        self.lottie_base = precomp
        self.analyze()

    @property
    def layers(self):
        return self._layers

    @layers.setter
    def layers(self, layers: list[Layer]):
        self._layers = layers
        self.lottie_base['layers'] = [layer.layer for layer in layers]

    @property
    def id(self):
        if 'id' in self.lottie_base:
            return self.lottie_base['id']
        else:
            return None

    @id.setter
    def id(self, precomp_id: str):
        self.lottie_base['id'] = ''
        self.lottie_element_id = precomp_id

    @property
    def name(self):
        if 'nm' in self.lottie_base:
            return self.lottie_base['nm']
        else:
            return None

    @name.setter
    def name(self, new_name):
        self.lottie_base['nm'] = new_name

    @property
    def framerate(self):
        if 'nm' in self.lottie_base:
            return self.lottie_base['fr']
        else:
            return None

    @framerate.setter
    def framerate(self, framerate):
        self.lottie_base['fr'] = framerate

    @property
    def main_layers_index(self):
        index = self._main_layers_index
        self._main_layers_index += 1
        return index

    def add_layer(self, new_layer: Layer, update_layer_id=True, order='last', layer_id: int = None):
        if update_layer_id:
            new_layer.id = self.main_layers_index
        layer_index = add_layer(self.layers, new_layer, order, layer_id)
        if layer_index is not None:
            self.lottie_base['layers'].insert(layer_index, new_layer.layer)

    def find_layer(self, layer_id: int = None, layer_name: str = None):
        find_layer(self._layers, layer_id, layer_name)

    def delete_layer(self, layer_id: int, layer_name: str = None):
        layer_index = delete_layer(self.layers, layer_id, layer_name)
        if layer_index is not None:
            self.lottie_base['layers'].remove(self.layers[layer_index].layer)

    def replace_layer(self, new_layer: Layer, layer_id=None, layer_name: str = None):
        layer_index = replace_layer(self.layers, new_layer, layer_id, layer_name)
        if layer_index is not None:
            self.lottie_base['layers'][layer_index] = new_layer.layer
