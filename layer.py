import copy
import enum
from transform import Transform


class Lottie_layer_type(enum.Enum):
    precomp = 0
    solid = 1
    image = 2
    null = 3
    shape = 4
    text = 5
    audio = 6
    pholder_video = 7
    image_seq = 8
    video = 9
    pholder_stil = 10
    guide = 11
    adjustment = 12
    camera = 13
    light = 14
    data = 15


class Layer:
    def __init__(self, layer_id: int = 0, layer_name: str = 'unknown', ddd_layer: int = 0, layer_parent=None,
                 layer_transform: Transform = None, reference_id=None, *args, **kwargs):
        self.layer = {}
        self._transform = Transform()
        self.id = layer_id
        self.name = layer_name
        self.ddd_layer = ddd_layer
        self.parent = layer_parent
        self.reference_id = reference_id
        self.transform = layer_transform
        self.analyze()

    def analyze(self):
        if type(self.layer) is not dict:
            raise TypeError("Error: layer is not of type dictionary")
        if self.id is None:
            raise TypeError("Error: layer doesn't have an id")
        if self.name is None:
            raise TypeError("Error: layer doesn't have a name")
        '''if self.type is None:
            raise TypeError("Error: layer doesn't have a type")'''

    def load(self, layer: dict):
        self.layer = layer
        if 'ks' in layer:
            self._transform = Transform()
            self._transform.load(layer['ks'])
        self.analyze()

    def copy(self, layer: dict):
        self.layer = copy.deepcopy(layer)
        self.analyze()

    @property
    def id(self):
        if 'ind' in self.layer:
            return self.layer['ind']
        else:
            return None

    @id.setter
    def id(self, layer_id: int):
        self.layer['ind'] = layer_id

    @property
    def name(self):
        if 'nm' in self.layer:
            return self.layer['nm']
        else:
            return None

    @name.setter
    def name(self, layer_name: str):
        self.layer['nm'] = layer_name

    @property
    def parent(self):
        if 'parent' in self.layer:
            return self.layer['parent']
        else:
            return None

    @parent.setter
    def parent(self, layer_parent: int):
        self.layer['parent'] = layer_parent

    @property
    def transform(self):
        return self._transform

    @transform.setter
    def transform(self, layer_transform: Transform):
        self._transform = layer_transform
        self.layer['ks'] = None if layer_transform is None else layer_transform.transform

    @property
    def reference_id(self):
        if 'refId' in self.layer:
            return self.layer['refId']
        else:
            return None

    @reference_id.setter
    def reference_id(self, new_transform):
        self.layer['refId'] = new_transform

    @property
    def type(self):
        if 'ty' in self.layer:
            return self.layer['ty']
        else:
            return None

    @type.setter
    def type(self, layer_type: int):
        self.layer['ty'] = layer_type

    @property
    def ddd_layer(self):
        if 'ddd' in self.layer:
            return self.layer['ddd']
        else:
            return None

    @ddd_layer.setter
    def ddd_layer(self, ddd_layer: int):
        self.layer['ddd'] = ddd_layer

    def parse_type(self):
        if 'ty' in self.layer:
            layer_type = self.layer["ty"]
            try:
                return Lottie_layer_type[layer_type]
            except ValueError:
                print("layer type doesn't exist")

    def hide(self):
        self.layer['hd'] = 0

    def reveal(self):
        self.layer['hd'] = 1

    def hidden(self):
        if 'hd' in self.layer and self.layer['hd']:
            return True
        else:
            return False

