import copy
from engine.layer import Layer, Lottie_layer_type
from engine.text_animator_data import Text_animator_data


class Text_layer(Layer):
    def __init__(self, layer_id: int = 0, layer_name: str = 'unknown', ddd_layer: int = 0, layer_parent=None,
                 layer_transform=None, reference_id=None, out_point: int = 30, text_data: Text_animator_data = None):
        Layer.__init__(self, layer_id, layer_name, ddd_layer, layer_parent, layer_transform, reference_id, out_point)
        self._textdata: Text_animator_data() = None
        self.type = Lottie_layer_type.Text
        self.textdata = text_data

    def analyze(self):
        Layer.analyze(self)
        if 't' not in self.lottie_base:
            raise TypeError("Error: text layer doesn't include textdata")

    def load(self, layer: dict):
        Layer.load(self, layer)
        self.analyze()
        self._textdata = Text_animator_data()
        self._textdata.load(layer['t'])

    def copy(self, layer: dict):
        self.lottie_base = copy.deepcopy(layer)

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
        self.lottie_base['t'] = textdata.text_animator_data


def refactor_font_name(layer: Text_layer, font_names_with_uuid: list[str]):
    for font_name_with_uuid in font_names_with_uuid:
        font_name = font_name_with_uuid.rsplit('_', 1)[0]
        for textdata in layer.textdata.text_boxes:
            if textdata.font_family == font_name:
                textdata.font_family = font_name_with_uuid
