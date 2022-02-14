from PIL import Image
from io import BytesIO

import copy
import base64
from helpers import generate_random_id, VIDALGO_ID


class Image_asset:
    def __init__(self, image_id: str = None, image_path: str = None, image_name: str = None, height: float = None,
                 width: float = None, embedded: int = 1):
        self.image = {}
        if image_id is not None:
            img = None
            try:
                img = Image.open(image_path)
                encoded = base64.b64encode(open(image_path, "rb").read())
                self.path = 'data:image/png;base64,' + encoded.decode("utf-8")
            except TypeError:
                print("Error: can't open image or image is not of the right format")
            self.id = image_id
            self.name = str(image_id) if image_name is None else image_name
            self.height = img.size[1] if height is None else height
            self.width = img.size[0] if width is None else width
            self.embedded = embedded
            self.analyze()

    def analyze(self):
        if type(self.image) is not dict:
            raise TypeError("Error: image is not of type dictionary")
        if self.id is None:
            raise TypeError("Error: image doesn't have an id")
        if self.path is None:
            raise TypeError("Error: image doesn't exist")
        if self.height is None:
            raise TypeError("Error: image height doesn't exist")
        if self.width is None:
            raise TypeError("Error: image width doesn't exist")
        if self.embedded is None or self.embedded != 0 and self.embedded != 1:
            raise TypeError("Error: image isn't embedded nor external")

    def load(self, image: dict):
        self.image = image
        self.analyze()

    def copy(self, image: dict):
        self.image = copy.deepcopy(image)
        self.analyze()

    @property
    def id(self):
        if 'id' in self.image:
            return self.image['id']
        else:
            return None

    @id.setter
    def id(self, image_id):
        self.image['id'] = image_id

    @property
    def name(self):
        if 'u' in self.image and self.image['u']:
            return self.image['u']
        else:
            return None

    @name.setter
    def name(self, image_name):
        if 'u' in self.image:
            self.image['u'] = image_name

    @property
    def path(self):
        if 'p' in self.image:
            return self.image['p']
        else:
            return None

    @path.setter
    def path(self, image_path: str):
        self.image['p'] = image_path

    @property
    def height(self):
        if 'h' in self.image:
            return self.image['h']
        else:
            return None

    @height.setter
    def height(self, new_height: float):
        self.image['h'] = new_height

    @property
    def width(self):
        if 'w' in self.image:
            return self.image['w']
        else:
            return None

    @width.setter
    def width(self, new_width: float):
        self.image['w'] = new_width

    @property
    def embedded(self):
        if 'e' in self.image:
            return self.image['e']
        else:
            return None

    @embedded.setter
    def embedded(self, is_embedded: bool):
        self.image['e'] = is_embedded
