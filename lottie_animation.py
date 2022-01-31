import copy
from lottie_search_and_replace import load_json, store_json
from image import Image
from precomp import Precomp
from layer import Layer
from os import path, makedirs

PATH = "/lottie_files_path/"


class Lottie_animation:
    def __init__(self, lottie_name: str = 'unknown', in_point: int = 1, out_point: int = 30, frame_rate: int = 30,
                 ddd_layers: int = 0, width: float = 500, height: float = 500):
        self.lottie_obj = {}
        self._layers: list[Layer] = []
        self._images: list[Image] = []
        self._precomp: list[Precomp] = []
        self._layer_id_counter = 0
        self._null_layer_id_counter = 1000
        self._pre_comb_id_counter = 10
        self.name = lottie_name
        self.width = width
        self.height = height
        self.frame_rate = frame_rate
        self.in_point = in_point
        self.out_point = out_point
        self.ddd_layers = ddd_layers
        self.layers = []
        self.assets = []
        self.analyze()
        '''self._fonts = []
        self._chars = []
        self._markers = []
        self._layers: list[Layer] = []'''

    def load(self, animation_file_name):
        self.lottie_obj = load_json(animation_file_name)
        self.analyze()
        self._layers = self.layers
        #self._assets = self.assets
        '''self._fonts = self.fonts
        self._chars = self.chars
        self._markers = self.main'''

    def store(self, file_name=None):
        if file_name is None:
            if not path.isdir(PATH):
                makedirs(PATH)
            file_name = "{0}{1}.json".format(PATH, self.name)
        store_json(file_name, self.lottie_obj)

    def copy(self, animation: dict):
        self.lottie_obj = copy.deepcopy(animation)
        self.analyze()

    def analyze(self):
        if type(self.lottie_obj) is not dict:
            raise TypeError("Error: composition is not of type dictionary")
        if self.name is None:
            raise TypeError("Error: composition doesn't have a name")
        if self.in_point is None:
            raise TypeError("Error: initial Frame of the animation is not set")
        if self.out_point is None:
            raise TypeError("Error: final Frame of the animation is not set")
        if self.frame_rate is None:
            raise TypeError("Error: Frame rate is not set")
        if self.ddd_layers is None or self.ddd_layers != 0 and self.ddd_layers != 1:
            raise TypeError("Error: 3d layers parameter is not set or erroneous")
        if self.width is None:
            raise TypeError("Error: Width is not set")
        if self.height is None:
            raise TypeError("Error: Height is not set")
        if self.layers is None:
            raise TypeError("Error: Animation layers not set")

    @property
    def name(self):
        if 'nm' in self.lottie_obj:
            return self.lottie_obj['nm']
        else:
            return None

    @name.setter
    def name(self, name: str):
        self.lottie_obj['nm'] = name

    @property
    def in_point(self):
        if 'ip' in self.lottie_obj:
            return self.lottie_obj['ip']
        else:
            return None

    @in_point.setter
    def in_point(self, in_point: int):
        self.lottie_obj['ip'] = in_point

    @property
    def out_point(self):
        if 'op' in self.lottie_obj:
            return self.lottie_obj['op']
        else:
            return None

    @out_point.setter
    def out_point(self, out_point: int):
        self.lottie_obj['op'] = out_point

    @property
    def frame_rate(self):
        if 'fr' in self.lottie_obj:
            return self.lottie_obj['fr']
        else:
            return None

    @frame_rate.setter
    def frame_rate(self, frame_rate: int):
        self.lottie_obj['fr'] = frame_rate

    @property
    def ddd_layers(self):
        if 'ddd' in self.lottie_obj:
            return self.lottie_obj['ddd']
        else:
            return None

    @ddd_layers.setter
    def ddd_layers(self, ddd_layers: int):
        self.lottie_obj['ddd'] = ddd_layers

    @property
    def width(self):
        if 'w' in self.lottie_obj:
            return self.lottie_obj['w']
        else:
            return None

    @width.setter
    def width(self, width: float):
        self.lottie_obj['w'] = width

    @property
    def height(self):
        if 'h' in self.lottie_obj:
            return self.lottie_obj['h']
        else:
            return None

    @height.setter
    def height(self, height: float):
        self.lottie_obj['h'] = height

    @property
    def bodymovin_version(self):
        if 'v' in self.lottie_obj:
            return self.lottie_obj['v']
        else:
            return None

    @bodymovin_version.setter
    def bodymovin_version(self, bodymovin_version: str):
        self.lottie_obj['v'] = bodymovin_version

    @property
    def layers(self):
        return self._layers

    @layers.setter
    def layers(self, lottie_layers: list[Layer]):
        self._layers = lottie_layers
        self.lottie_obj['layers'] = [lottie_layer.layer for lottie_layer in lottie_layers]

    @property
    def assets(self):
        if 'assets' in self.lottie_obj:
            return self.lottie_obj['assets']
        else:
            return None

    @assets.setter
    def assets(self, assets: list):
        self.lottie_obj['assets'] = assets

    @property
    def images(self):
        return self._images

    @images.setter
    def images(self, images: list[Image]):
        self._images = images
        pre_comps_temp = [pre_comp for pre_comp in self.lottie_obj['assets'] if type(pre_comp) == Precomp]
        self.lottie_obj['assets'] = [image.image for image in images] + pre_comps_temp

    def add_image(self, image: Image):
        self.images.insert(0, image)
        self.lottie_obj['assets'].insert(0, image.image)

    def find_image(self, image_id):
        for image in self.images:
            if image.id == image_id:
                return image
        return None

    def delete_image(self, image_id):
        image = self.find_image(image_id)
        if image is not None:
            self.images.remove(image)
            self.lottie_obj['assets'].remove(image.image)

    def replace_image(self, image: Image, replaced_image_id):
        for index, image in enumerate(self.images):
            if image.id == replaced_image_id:
                self.images[index] = image
                self.lottie_obj['assets'][index] = image.image
                break

    def add_main_layer(self, new_layer: Layer, update_layer_id=True, order='last', layer_id: int = None):
        if update_layer_id:
            new_layer.id = self._layer_id_counter
            self._layer_id_counter += 1
        if order == 'first':
            self.layers.insert(0, new_layer)
            self.lottie_obj['layers'].insert(0, new_layer.layer)
        elif order == 'last':
            self.layers.append(new_layer)
            self.lottie_obj['layers'].append(new_layer.layer)
        else:
            for index, layer in enumerate(self.lottie_obj['layers']):
                if layer["ind"] == layer_id:
                    if order == 'before':
                        self.layers.insert(index, new_layer)
                        self.lottie_obj['layers'].insert(index, new_layer.layer)
                        break
                    elif order == 'after':
                        self.layers.insert(index + 1, new_layer)
                        self.lottie_obj['layers'].insert(index + 1, new_layer.layer)
                        break

    def find_main_layer(self, layer_id: int):
        for index, layer in enumerate(self.layers):
            if layer.id == layer_id:
                return [index, layer]
        return [None, None]

    def delete_main_layer(self, layer_id: int):
        [index, main_layer] = self.find_main_layer(layer_id)
        if main_layer is not None:
            self.layers.remove(main_layer)
            self.lottie_obj['layers'].remove(main_layer.layer)

    def replace_main_layer(self, new_layer: Layer, replaced_layer_id):
        for index, layer in enumerate(self.layers):
            if layer.id == replaced_layer_id:
                self.layers[index] = new_layer
                self.lottie_obj['layers'][index] = new_layer.layer
                break

    '''@property
    def fonts(self):
        if 'fonts' in self.main:
            return self.main['fonts']
        else:
            return None

    @fonts.setter
    def fonts(self, fonts: list):
        self.main['fonts'] = fonts

    @property
    def chars(self):
        if 'chars' in self.main:
            return self.main['chars']
        else:
            return None

    @chars.setter
    def chars(self, lottie_chars: list):
        self.main['chars'] = lottie_chars

    @property
    def markers(self):
        if 'markers' in self.main:
            return self.main['markers']
        else:
            return None

    @markers.setter
    def markers(self, lottie_markers: list):
        self.main['markers'] = lottie_markers'''
