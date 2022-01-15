class Layer:
    def __init__(self, layer):
        self.layer = layer
        if not dict(layer):
            raise TypeError("Error: layer is not of type dictionary")

    @property
    def id(self):
        if 'ind' in self.layer:
            return self.layer['ind']
        else:
            return None

    @id.setter
    def id(self, new_id):
        self.layer['ind'] = new_id

    @property
    def name(self):
        if 'nm' in self.layer:
            return self.layer['nm']
        else:
            return None

    @name.setter
    def name(self, new_name):
        self.layer['nm'] = new_name

    @property
    def parent(self):
        if 'parent' in self.layer:
            return self.layer['parent']
        else:
            return None

    @parent.setter
    def parent(self, new_parent):
        self.layer['parent'] = new_parent

    @property
    def transform(self):
        if 'ks' in self.layer:
            return self.layer['ks']
        else:
            return None

    @transform.setter
    def transform(self, new_transform):
        self.layer['ks'] = new_transform

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
    def type(self, new_type):
        self.layer['ty'] = new_type

    def parse_type(self):
        if 'ty' in self.layer:
            layer_type = self.layer["ty"]
            if layer_type == 0:
                return 'precomp'
            elif layer_type == 1:
                return 'solid'
            elif layer_type == 2:
                return 'image'
            elif layer_type == 3:
                return 'nullLayer'
            elif layer_type == 4:
                return 'shape'
            elif layer_type == 5:
                return 'text'
            elif layer_type == 6:
                return 'audio'
            elif layer_type == 7:
                return 'pholderVideo'
            elif layer_type == 8:
                return 'imageSeq'
            elif layer_type == 9:
                return 'video'
            elif layer_type == 10:
                return 'pholderStil'
            elif layer_type == 11:
                return 'guide'
            elif layer_type == 12:
                return 'adjustment'
            elif layer_type == 13:
                return 'camera'
            elif layer_type == 14:
                return 'light'
            elif layer_type == 15:
                return 'data'
            else:
                return 'unknown'
        return None

    def hide(self):
        self.layer['hd'] = 0

    def reveal(self):
        self.layer['hd'] = 1

    def hidden(self):
        if 'hd' in self.layer and self.layer['hd']:
            return True
        else:
            return False

