class Image:
    def __init__(self, image):
        self.image = image
        if type(image) is not dict:
            raise TypeError("Error: pre-composition is not of type dictionary")

    @property
    def id(self):
        if 'id' in self.image:
            return self.image['id']
        else:
            return None

    @id.setter
    def id(self, new_id):
        self.image['id'] = new_id

    @property
    def name(self):
        if 'u' in self.image and self.image['u']:
            return self.image['u']
        else:
            return None

    @name.setter
    def name(self, new_name):
        self.image['u'] = new_name

    @property
    def path(self):
        if 'p' in self.image:
            return self.image['p']
        else:
            return None

    @path.setter
    def path(self, new_name):
        self.image['p'] = new_name

    @property
    def height(self):
        if 'h' in self.height:
            return self.height['h']
        else:
            return None

    @height.setter
    def height(self, new_height: float):
        self.height['h'] = new_height

    @property
    def width(self):
        if 'w' in self.width:
            return self.width['w']
        else:
            return None

    @width.setter
    def width(self, new_width: float):
        self.width['w'] = new_width

    @property
    def embedded(self):
        if 'e' in self.embedded:
            return self.embedded['e']
        else:
            return None

    @embedded.setter
    def embedded(self, is_embedded: bool):
        self.embedded['e'] = is_embedded
