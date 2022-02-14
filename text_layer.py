import copy
from layer import Layer, Lottie_layer_type
from text_animator_data import Text_animator_data


class Text_layer(Layer):
    def __init__(self, layer_id: int = 0, layer_name: str = 'unknown', ddd_layer: int = 0, layer_parent=None,
                 layer_transform=None, reference_id=None, text_data: Text_animator_data = None):
        Layer.__init__(self, layer_id, layer_name, ddd_layer, layer_parent, layer_transform, reference_id)
        self._textdata:Text_animator_data = None
        self.type = Lottie_layer_type.Text.value
        self.textdata = text_data

    def analyze(self):
        Layer.analyze(self)
        if 't' not in self._layer:
            raise TypeError("Error: text layer doesn't include textdata")

    def load(self, layer: dict):
        Layer.load(self, layer)
        self.analyze()
        self._textdata = Text_animator_data()
        self._textdata.load(layer['t'])

    def copy(self, layer: dict):
        self._layer = copy.deepcopy(layer)

    @property
    def text(self):
        return self.textdata.text

    @text.setter
    def text(self, text_data: str):
        self.textdata.text = text_data

    @property
    def textdata(self):
        return self._textdata

    @textdata.setter
    def textdata(self, textdata: Text_animator_data):
        if textdata is None:
            textdata = Text_animator_data()
        self._textdata = textdata
        self._layer['t'] = textdata.text_animator_data


def update_font_name(layers: list, font_name: str, updated_font_name: str):
    for layer in layers:
        if layer.type == Lottie_layer_type.Text:
            for textdata in layer.textdata.text_boxes:
                if textdata.font_family == font_name:
                    textdata.font_family = updated_font_name


