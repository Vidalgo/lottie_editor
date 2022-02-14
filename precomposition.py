import copy
import helpers
from helpers import generate_random_id, VIDALGO_ID
from layer import Layer, Lottie_layer_type, find_layer, add_layer, delete_layer, replace_layer


class Precomposition:
    def __init__(self, precomp_id: str = None, precomp_name: str = None, framerate: float = 30):
        self._precomp = {}
        self._layers = []
        self.id = precomp_id
        self.name = precomp_name
        self.framerate = framerate
        generate_random_id(self._precomp)

    def load(self, precomp: dict):
        def _load_layer(layer: dict):
            layer_type = '{0}_layer'.format(Lottie_layer_type(Layer.get_type(layer)).name)
            new_layer = globals()[layer_type]() if layer_type in globals() else Layer()
            new_layer.load(layer)
            return new_layer

        self._precomp = precomp
        self.analyze()
        self._layers = [] if 'layers' not in precomp else [_load_layer(layer) for layer in self._precomp['layers']]
        if helpers.VIDALGO_ID not in precomp:
            generate_random_id(self._precomp)

    def copy(self, animation: dict):
        self._precomp = copy.deepcopy(animation)
        self.analyze()

    def analyze(self):
        if type(self._precomp) is not dict:
            raise TypeError("Error: precomposition is not of type dictionary")
        if self.id is None:
            raise TypeError("Error: precomposition id is missing")

    @property
    def vidalgo_id(self):
        if VIDALGO_ID in self._precomp:
            return self._precomp[VIDALGO_ID]
        else:
            return None

    @vidalgo_id.setter
    def vidalgo_id(self, vidalgo_id: str):
        self._precomp[VIDALGO_ID] = vidalgo_id

    @property
    def precomp(self):
        return self._precomp

    @precomp.setter
    def precomp(self, precomp: dict):
        self._precomp = precomp
        self.analyze()

    @property
    def layers(self):
        return self._layers

    @layers.setter
    def layers(self, layers: list[Layer]):
        self._layers = layers
        self._precomp['layers'] = [layer.layer for layer in layers]

    @property
    def id(self):
        if 'id' in self._precomp:
            return self._precomp['id']
        else:
            return None

    @id.setter
    def id(self, precomp_id: str):
        self._precomp['id'] = precomp_id

    @property
    def name(self):
        if 'nm' in self._precomp:
            return self._precomp['nm']
        else:
            return None

    @name.setter
    def name(self, new_name):
        self._precomp['nm'] = new_name

    @property
    def framerate(self):
        if 'nm' in self._precomp:
            return self._precomp['fr']
        else:
            return None

    @framerate.setter
    def framerate(self, framerate):
        self._precomp['fr'] = framerate

    def add_layer(self, new_layer: Layer, update_layer_id=True, order='last', layer_id: int = None):
        layer_index = add_layer(self.layers, new_layer, order, layer_id)
        if layer_index is not None:
            self._precomp['layers'].insert(layer_index, new_layer.layer)

    def find_layer(self, layer_id: int = None, layer_name: str = None):
        find_layer(self._layers, layer_id, layer_name)

    def delete_layer(self, layer_id: int, layer_name: str = None):
        layer_index = delete_layer(self.layers, layer_id, layer_name)
        if layer_index is not None:
            self._precomp['layers'].remove(self.layers[layer_index].layer)

    def replace_layer(self, new_layer: Layer, layer_id=None, layer_name: str = None):
        layer_index = replace_layer(self.layers, new_layer, layer_id, layer_name)
        if layer_index is not None:
            self._precomp['layers'][layer_index] = new_layer.layer
