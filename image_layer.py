from layer import Layer, Lottie_layer_type


class Image_layer(Layer):
    def __init__(self, layer_id: int = 0, layer_name: str = 'unknown', ddd_layer: int = 0, layer_parent=None,
                 layer_transform=None, reference_id=None, out_point: int = 30):
        Layer.__init__(self, layer_id, layer_name, ddd_layer, layer_parent, layer_transform, reference_id, out_point)
        self.type = Lottie_layer_type.Image

    def analyze(self):
        Layer.analyze(self)
        if self.reference_id is None:
            raise TypeError("Error: image layer doesn't reference an image")
