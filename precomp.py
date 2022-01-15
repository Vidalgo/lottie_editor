from layer import Layer


class Precomp:
    def __init__(self, precomp):
        self.precomp = precomp
        if type(precomp) is not dict:
            raise TypeError("Error: pre-composition is not of type dictionary")
        self.layers = []

    @property
    def id(self):
        if 'id' in self.precomp:
            return self.precomp['id']
        else:
            return None

    @id.setter
    def id(self, new_id):
        self.precomp['id'] = new_id

    @property
    def name(self):
        if 'nm' in self.precomp:
            return self.precomp['nm']
        else:
            return None

    @name.setter
    def name(self, new_name):
        self.precomp['nm'] = new_name

    def set_layer(self, new_layer: Layer, where='last', existing_layer_id=None):
        if where == 'last':
            self.layers.insert(-1, new_layer)
            self.precomp['layers'].insert(-1, new_layer.layer)
        elif where == 'first':
            self.layers.insert(0, new_layer)
            self.precomp['layers'].insert(0, new_layer.layer)
        elif where == 'before':
            index = self.get_layer(existing_layer_id)
            if index is not None:
                if where == 'before':
                    self.layers.insert(index, new_layer)
                    self.precomp['layers'].insert(index, new_layer.layer)
                elif where == 'after':
                    self.layers.insert(index+1, new_layer)
                    self.precomp['layers'].insert(index+1, new_layer.layer)

    def get_layer(self, layer_id):
        for index, layer in enumerate(self.layers):
            if Layer(layer).id == layer_id:
                return index
        return None

    def delete_layer(self, layer_id):
        for index, layer in enumerate(self.layers):
            if Layer(layer).id == layer_id:
                del self.layers[index + 1]
                del self.precomp['layers'][index + 1]
