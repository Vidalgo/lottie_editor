from PIL import Image
from io import BytesIO

import copy
import base64

from vidalgo_lottie_base import Vidalgo_lottie_base


class Image_asset(Vidalgo_lottie_base):
    def __init__(self, image_id: str = None, image_path: str = None, image_name: str = None, height: float = None,
                 width: float = None, embedded: int = 1):
        super(Image_asset, self).__init__()
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
        super(Image_asset, self).analyze()
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
        self.lottie_base = image
        self.analyze()

    def copy(self, image: dict):
        super(Image_asset, self).copy()
        self.analyze()

    @property
    def image(self):
        return self.lottie_base

    @image.setter
    def image(self, image):
        self.lottie_base = image
        self.analyze()

    @property
    def id(self):
        if 'id' in self.lottie_base:
            return self.lottie_base['id']
        else:
            return None

    @id.setter
    def id(self, image_id):
        self.lottie_base['id'] = ''
        self.lottie_element_id = image_id

    @property
    def name(self):
        if 'u' in self.lottie_base and self.lottie_base['u']:
            return self.lottie_base['u']
        else:
            return None

    @name.setter
    def name(self, image_name):
        if 'u' in self.lottie_base:
            self.lottie_base['u'] = image_name

    @property
    def path(self):
        if 'p' in self.lottie_base:
            return self.lottie_base['p']
        else:
            return None

    @path.setter
    def path(self, image_path: str):
        self.lottie_base['p'] = image_path

    @property
    def height(self):
        if 'h' in self.lottie_base:
            return self.lottie_base['h']
        else:
            return None

    @height.setter
    def height(self, new_height: float):
        self.lottie_base['h'] = new_height

    @property
    def width(self):
        if 'w' in self.lottie_base:
            return self.lottie_base['w']
        else:
            return None

    @width.setter
    def width(self, new_width: float):
        self.lottie_base['w'] = new_width

    @property
    def embedded(self):
        if 'e' in self.lottie_base:
            return self.lottie_base['e']
        else:
            return None

    @embedded.setter
    def embedded(self, is_embedded: bool):
        self.lottie_base['e'] = is_embedded
