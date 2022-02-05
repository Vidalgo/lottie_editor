from layer import Layer, Lottie_layer_type


class Image_layer(Layer):
    def __init__(self, layer_id: int = 0, layer_name: str = 'unknown', ddd_layer: int = 0, layer_parent=None,
                 layer_transform=True, reference_id=None, in_point: float = 0, out_point: float = 0,
                 auto_orient: float = None, blend_mode: float = 0, layer_class: str = None, layer_html_id: str = None,
                 start_time: float = 0, has_mask=None, masks_properties: list = None, effects: list = None,
                 stretch: float = 1):
        Layer.__init__(self, layer_id, layer_name, ddd_layer, layer_parent, layer_transform, reference_id)
        self.type = Lottie_layer_type.Image.value
        self.auto_orient = auto_orient
        self.blend_mode = blend_mode
        self.layer_class = layer_class
        self.layer_html_id = layer_html_id
        self.in_point = in_point
        self.out_point = out_point
        self.start_time = start_time
        self.has_mask = has_mask
        self.masks_properties = masks_properties
        self.effects = effects
        self.stretch = stretch

    def analyze(self):
        Layer.analyze(self)
        if self.reference_id is None:
            raise TypeError("Error: image layer doesn't reference an image")

    @property
    def auto_orient(self):
        if 'ao' in self.layer:
            return self.layer['ao']
        else:
            return None

    @auto_orient.setter
    def auto_orient(self, auto_orient: float):
        self.layer['ao'] = auto_orient

    @property
    def blend_mode(self):
        if 'bm' in self.layer:
            return self.layer['bm']
        else:
            return None

    @blend_mode.setter
    def blend_mode(self, blend_mode: float):
        self.layer['bm'] = blend_mode

    @property
    def layer_class(self):
        if 'cl' in self.layer:
            return self.layer['cl']
        else:
            return None

    @layer_class.setter
    def layer_class(self, layer_class: str):
        self.layer['cl'] = layer_class

    @property
    def layer_html_id(self):
        if 'ln' in self.layer:
            return self.layer['ln']
        else:
            return None

    @layer_html_id.setter
    def layer_html_id(self, layer_html_id: str):
        self.layer['ln'] = layer_html_id

    @property
    def in_point(self):
        if 'ip' in self.layer:
            return self.layer['ip']
        else:
            return None

    @in_point.setter
    def in_point(self, in_point: float):
        self.layer['ip'] = in_point

    @property
    def out_point(self):
        if 'op' in self.layer:
            return self.layer['op']
        else:
            return None

    @out_point.setter
    def out_point(self, out_point: float):
        self.layer['op'] = out_point

    @property
    def start_time(self):
        if 'st' in self.layer:
            return self.layer['st']
        else:
            return None

    @start_time.setter
    def start_time(self, start_time: float):
        self.layer['st'] = start_time

    @property
    def has_mask(self):
        if 'hasMask' in self.layer:
            return self.layer['hasMask']
        else:
            return None

    @has_mask.setter
    def has_mask(self, has_mask: float):
        self.layer['hasMask'] = has_mask

    @property
    def masks_properties(self):
        if 'hasMask' in self.layer:
            return self.layer['hasMask']
        else:
            return None

    @masks_properties.setter
    def masks_properties(self, masks_properties: list):
        self.layer['hasMask'] = masks_properties

    @property
    def effects(self):
        if 'ef' in self.layer:
            return self.layer['ef']
        else:
            return None

    @effects.setter
    def effects(self, effects: list):
        self.layer['ef'] = effects

    @property
    def stretch(self):
        if 'sr' in self.layer:
            return self.layer['sr']
        else:
            return None

    @stretch.setter
    def stretch(self, stretch: list):
        self.layer['sr'] = stretch
