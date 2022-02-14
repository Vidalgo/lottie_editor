from layer import Layer, Lottie_layer_type


class Image_layer(Layer):
    def __init__(self, layer_id: int = 0, layer_name: str = 'unknown', ddd_layer: int = 0, layer_parent=None,
                 layer_transform=None, reference_id=None):
        Layer.__init__(self, layer_id, layer_name, ddd_layer, layer_parent, layer_transform, reference_id)
        self.type = Lottie_layer_type.Image.value

    def analyze(self):
        Layer.analyze(self)
        if self.reference_id is None:
            raise TypeError("Error: image layer doesn't reference an image")
