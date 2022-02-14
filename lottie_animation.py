from __future__ import annotations
import random


from font import Font
from char import Char
from image_asset import Image_asset
from precomposition import Precomposition
from layer import Layer, Lottie_layer_type, find_layer, add_layer, delete_layer, replace_layer, update_ref_id
from precomp_layer import Precomp_layer
from text_layer import update_font_name





'''self._chars = []
    self._markers = []
    self._layers: list[Layer] = []'''


class Lottie_animation:
    def __init__(self, lottie_name: str = 'unknown', in_point: int = 0, out_point: int = 30, frame_rate: int = 30,
                 ddd_layers: int = 0, width: float = 500, height: float = 500, version: str = "5.5.2"):
        self._lottie_obj = {}
        self._fonts: list[Font] = []
        self._chars: list[Char] = []
        self._layers: list[Layer] = []
        self._images: list[Image_asset] = []
        self._precomp: list[Precomposition] = []
        self._id_counter = 0
        self._null_layer_id_counter = 1000
        self._pre_comb_id_counter = 10
        self.version = version
        self.name = lottie_name
        self.width = width
        self.height = height
        self.frame_rate = frame_rate
        self.in_point = in_point
        self.out_point = out_point
        self.ddd_layers = ddd_layers
        self.assets = []
        generate_random_id(self._lottie_obj)

    def _refactor_ids(self):
        self._id_counter = 0
        layers_ids_dictionary = {}
        pre_comp_ids_dictionary = {}
        images_comp_ids_dictionary = {}
        for layer in self.layers:
            layers_ids_dictionary[layer.id] = self._id_counter
            layer.id = self._id_counter
            self._id_counter += 1
        for asset in self.assets:
            refactored_id = "{0}_{1}".format(asset['id'], str(self._id_counter))
            if 'id' in asset:
                pre_comp_ids_dictionary[asset['id']] = refactored_id
            elif 'e' in asset:
                images_comp_ids_dictionary[asset['id']] = refactored_id
            asset['id'] = refactored_id
            self._id_counter += 1
        for layer in self.layers:
            if layer.parent is not None:
                layer.parent = layers_ids_dictionary[layer.parent]
            if layer.reference_id is not None:
                if layer.reference_id in pre_comp_ids_dictionary:
                    layer.reference_id = pre_comp_ids_dictionary[layer.reference_id]
                else:
                    layer.reference_id = images_comp_ids_dictionary[layer.reference_id]

    def _update_ref_id(self, layer_type: Lottie_layer_type, ref_id: str, updated_ref_id: str):
        for pre_comp in self.precomp:
            update_ref_id(pre_comp.layers, layer_type, ref_id, updated_ref_id)
        update_ref_id(self.layers, layer_type, ref_id, updated_ref_id)

    def _adjust_precompositions_intersection(self, animation: Lottie_animation):
        precomp_id_intersections = update_intersected_ids(animation.precomp, self.precomp)
        for precomp_id in precomp_id_intersections:
            self._update_ref_id(Lottie_layer_type.Precomp, precomp_id, '{0}{1}'.format(precomp_id, ID_SUFFIX))

    def _adjust_images_intersection(self, animation: Lottie_animation):
        image_id_intersections = update_intersected_ids(animation.images, self.images)
        for image_id in image_id_intersections:
            self._update_ref_id(Lottie_layer_type.Image, image_id, '{0}{1}'.format(image_id, ID_SUFFIX))

    def _adjust_fonts_intersection(self, animation: Lottie_animation):
        font_id_intersections = update_intersected_ids(animation.fonts, self.images)
        for font_id in font_id_intersections:
            self._update_ref_id(Lottie_layer_type.Text, font_id, '{0}{1}'.format(font_id, ID_SUFFIX))

    def __add__(self, animation: Lottie_animation):
        self._adjust_precompositions_intersection(animation)
        self._adjust_images_intersection(animation)
        self._adjust_fonts_intersection(animation)
        # self._adjust_characters_intersection(animation)
        # markers : no check needed
        # motion blur : use destination but issue a warning if source motion blur exists
        self.in_point = min(self.in_point, animation.in_point)
        self.out_point = max(self.out_point, animation.out_point)
        self.width += animation.width
        self.height += animation.height
        self.ddd_layers = max(self.ddd_layers, animation.ddd_layers)
        self.assets += animation.assets
        self.fonts += animation.fonts
        # self.chars += animation.chars
        # self.markers += animation.markers
        # update metadata (consult Github)
        this_precomp = Precomposition(precomp_id=self.name, framerate=self.frame_rate)
        this_precomp.layers = self.layers
        animation_precomp = Precomposition(precomp_id=animation.name, framerate=animation.frame_rate)
        animation_precomp.layers = animation.layers
        self.add_precomp(this_precomp)
        self.add_precomp(animation_precomp)
        this_main_layer = Precomp_layer(layer_name=self.name, layer_id=0, reference_id=self.name, width=self.width,
                                        height=self.height, layer_transform=True)
        animation_main_layer = Precomp_layer(layer_name=animation.name, layer_id=1, reference_id=animation.name,
                                             width=animation.width, height=animation.height, layer_transform=True)
        animation_main_layer.transform.position = [self.width, self.height, 0]
        self.layers = [this_main_layer, animation_main_layer]
        #self._refactor_ids()
        return self

    def load(self, animation_file_name):
        def _load_font(font: dict):
            new_font = Font()
            new_font.load(font)
            return new_font

        def _load_char(char: dict):
            new_char = Char()
            new_char.load(char)
            return new_char

        def _load_layer(layer: dict):
            layer_type = '{0}_layer'.format(Lottie_layer_type(Layer.get_type(layer)).name)
            new_layer = globals()[layer_type]() if layer_type in globals() else Layer()
            new_layer.load(layer)
            return new_layer

        def _load_asset():
            if 'assets' in self._lottie_obj and self._lottie_obj['assets'] is not None:
                for asset in self._lottie_obj['assets']:
                    if 'e' in asset:
                        new_asset = Image_asset()
                        new_asset.load(asset)
                        self._images.append(new_asset)
                    else:
                        new_asset = Precomposition()
                        new_asset.load(asset)
                        self._precomp.append(new_asset)

        self._lottie_obj = load_json(animation_file_name)
        self.analyze()
        self._fonts = [] if 'fonts' not in self._lottie_obj or 'list' not in self._lottie_obj['fonts'] else\
            [_load_font(font) for font in self._lottie_obj['fonts']['list']]
        self._chars = [] if 'chars' not in self._lottie_obj else \
            [_load_char(char) for char in self._lottie_obj['chars']]
        self._layers = [_load_layer(layer) for layer in self._lottie_obj['layers']]
        _load_asset()
        # self._assets = self.assets
        '''self._fonts = self.fonts
        self._chars = self.chars
        self._markers = self.main'''

    def store(self, file_name=None):
        if file_name is None:
            if not path.isdir(PATH):
                makedirs(PATH)
            file_name = "{0}{1}.json".format(PATH, self.name)
        store_json(file_name, self._lottie_obj)

    def copy(self, animation: dict):
        self._lottie_obj = copy.deepcopy(animation)
        self.analyze()

    def analyze(self):
        if type(self._lottie_obj) is not dict:
            raise TypeError("Error: composition is not of type dictionary")
        if self.version is None:
            raise TypeError("Error: lottie version is missing")
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
    def lottie(self):
        return self._lottie_obj

    @lottie.setter
    def lottie(self, lottie: dict):
        self._lottie_obj = lottie
        self.analyze()

    @property
    def name(self):
        if 'nm' in self._lottie_obj:
            return self._lottie_obj['nm']
        else:
            return None

    @name.setter
    def name(self, name: str):
        self._lottie_obj['nm'] = name

    @property
    def version(self):
        if 'v' in self._lottie_obj:
            return self._lottie_obj['v']
        else:
            return None

    @version.setter
    def version(self, version: str):
        self._lottie_obj['v'] = version

    @property
    def match_name(self):
        if 'mn' in self._lottie_obj:
            return self._lottie_obj['mn']
        else:
            return None

    @match_name.setter
    def match_name(self, match_name: str):
        self._lottie_obj['mn'] = match_name

    @property
    def in_point(self):
        if 'ip' in self._lottie_obj:
            return self._lottie_obj['ip']
        else:
            return None

    @in_point.setter
    def in_point(self, in_point: int):
        self._lottie_obj['ip'] = in_point

    @property
    def out_point(self):
        if 'op' in self._lottie_obj:
            return self._lottie_obj['op']
        else:
            return None

    @out_point.setter
    def out_point(self, out_point: int):
        self._lottie_obj['op'] = out_point

    @property
    def frame_rate(self):
        if 'fr' in self._lottie_obj:
            return self._lottie_obj['fr']
        else:
            return None

    @frame_rate.setter
    def frame_rate(self, frame_rate: int):
        self._lottie_obj['fr'] = frame_rate

    @property
    def ddd_layers(self):
        if 'ddd' in self._lottie_obj:
            return self._lottie_obj['ddd']
        else:
            return None

    @ddd_layers.setter
    def ddd_layers(self, ddd_layers: int):
        self._lottie_obj['ddd'] = ddd_layers

    @property
    def width(self):
        if 'w' in self._lottie_obj:
            return self._lottie_obj['w']
        else:
            return None

    @width.setter
    def width(self, width: float):
        self._lottie_obj['w'] = width

    @property
    def height(self):
        if 'h' in self._lottie_obj:
            return self._lottie_obj['h']
        else:
            return None

    @height.setter
    def height(self, height: float):
        self._lottie_obj['h'] = height

    @property
    def bodymovin_version(self):
        if 'v' in self._lottie_obj:
            return self._lottie_obj['v']
        else:
            return None

    @bodymovin_version.setter
    def bodymovin_version(self, bodymovin_version: str):
        self._lottie_obj['v'] = bodymovin_version

    @property
    def fonts(self):
        return self._fonts

    @fonts.setter
    def fonts(self, fonts: list[Font]):
        self._fonts = fonts
        if 'font' not in self._lottie_obj:
            self._lottie_obj['fonts'] = {}
        self._lottie_obj['fonts']['list'] = [font.font for font in fonts]

    def add_font(self, font: Font):
        if 'fonts' not in self._lottie_obj:
            self._lottie_obj['fonts'] = {'list': []}
        else:
            for fonts in self.fonts:
                if fonts.font_name == font.font_name:
                    return
        self.fonts.insert(0, font)
        self._lottie_obj['fonts']['list'].insert(0, font.font)

    def find_font(self, font_name: str):
        for font in self.fonts:
            if font.font_name == font_name:
                return font
        return None

    def delete_font(self, font_name: str):
        font = self.find_font(font_name)
        if font is not None:
            self.fonts.remove(font)
            self._lottie_obj['fonts']['list'].remove(font.font)

    def replace_font(self, new_font: Font, replaced_font_name):
        for index, font in enumerate(self.fonts):
            if font.font_name == replaced_font_name:
                self.fonts[index] = new_font
                self._lottie_obj['fonts']['list'][index] = new_font.font
                update_font_name(self.layers, Lottie_layer_type.Text, replaced_font_name, new_font.font_name)
                for precomp_ref in self.precomp:
                    update_font_name(precomp_ref.layers, Lottie_layer_type.Text, replaced_font_name, new_font.font_name)
                break

    @property
    def chars(self):
        return self._chars

    @chars.setter
    def chars(self, chars: list[Char]):
        self._chars = chars
        if 'chars' not in self._lottie_obj:
            self._lottie_obj['chars'] = {}
        self._lottie_obj['chars'] = [char.char for char in chars]

    def add_char(self, char: Char):
        if 'chars' not in self._lottie_obj:
            self._lottie_obj['chars'] = None
        else:
            for chars in self.chars:
                if chars.character == char.character:
                    return
        self.chars.insert(0, char)
        self._lottie_obj['chars'].insert(0, char.char)

    def find_char(self, char_name: str):
        for char in self.chars:
            if char.character == char_name:
                return char
        return None

    def delete_char(self, char_name: str):
        char = self.find_char(char_name)
        if char is not None:
            self.chars.remove(char)
            self._lottie_obj['chars'].remove(char.character)

    def replace_char(self, new_char: Char, replaced_char_name):
        for index, char in enumerate(self.chars):
            if char.character == replaced_char_name:
                self.chars[index] = new_char
                self._lottie_obj['chars'][index] = new_char.character
                for font in self.fonts:
                    if font.font_family == char.font_family:
                        font.font_family = new_char.font_family
                break

    @property
    def layers(self):
        return self._layers

    @layers.setter
    def layers(self, lottie_layers: list[Layer]):
        self._layers = lottie_layers
        self._lottie_obj['layers'] = [lottie_layer.layer for lottie_layer in lottie_layers]

    @property
    def assets(self):
        if 'assets' in self._lottie_obj:
            return self._lottie_obj['assets']
        else:
            return None

    @assets.setter
    def assets(self, assets: list):
        self._lottie_obj['assets'] = assets

    @property
    def images(self):
        return self._images

    @images.setter
    def images(self, images: list[Image_asset]):
        self._images = images
        pre_comps_temp = [pre_comp for pre_comp in self._lottie_obj['assets'] if type(pre_comp) == Precomposition]
        self._lottie_obj['assets'] = [image.image for image in images] + pre_comps_temp

    def add_image(self, image: Image_asset):
        self.images.insert(0, image)
        self._lottie_obj['assets'].insert(0, image.image)

    def find_image(self, image_id):
        for image in self.images:
            if image.id == image_id:
                return image
        return None

    def delete_image(self, image_id):
        image = self.find_image(image_id)
        if image is not None:
            self.images.remove(image)
            self._lottie_obj['assets'].remove(image.image)

    def replace_image(self, new_image: Image_asset, replaced_image_id):
        for index, image in enumerate(self.images):
            if image.id == replaced_image_id:
                self.images[index] = new_image
                self._lottie_obj['assets'][index] = new_image.image
                update_ref_id(self.layers, Lottie_layer_type.Precomp, replaced_image_id, new_image.id)
                for precomp_ref in self.precomp:
                    update_ref_id(precomp_ref.layers, Lottie_layer_type.Image, replaced_image_id, new_image.id)
                break

    @property
    def precomp(self):
        return self._precomp

    @precomp.setter
    def precomp(self, precomps: list[Precomposition]):
        self._precomp = precomps
        images_temp = [image for image in self._lottie_obj['assets'] if type(image) == Image_asset]
        self._lottie_obj['assets'] = images_temp + [precomp.precomp for precomp in precomps]

    def add_precomp(self, precomp: Precomposition):
        self.precomp.insert(0, precomp)
        self._lottie_obj['assets'].append(precomp.precomp)

    def find_precomb(self, precomb_id):
        for precomb in self.precomp:
            if precomb.id == precomb_id:
                return precomb
        return None

    def delete_precomb(self, precomb_id):
        precomp = self.find_precomb(precomb_id)
        if precomp is not None:
            self.precomp.remove(precomp)
            self._lottie_obj['assets'].remove(precomp.precomp)

    def replace_precomp(self, new_precomp: Precomposition, replaced_precomp_id):
        for index, precomp in enumerate(self.precomp):
            if precomp.id == replaced_precomp_id:
                self.precomp[index] = new_precomp
                self._lottie_obj['assets'][index] = new_precomp.precomp
                update_ref_id(self.layers, Lottie_layer_type.Precomp, replaced_precomp_id, new_precomp.id)
                for precomp_ref in self.precomp:
                    update_ref_id(precomp_ref.layers, Lottie_layer_type.Precomp, replaced_precomp_id, new_precomp.id)
                break

    def add_main_layer(self, new_layer: Layer, update_layer_id=True, order='last', layer_id: int = None):
        if update_layer_id:
            new_layer.id = self._id_counter
            self._id_counter += 1
        layer_index = add_layer(self.layers, new_layer, order, layer_id)
        if layer_index is not None:
            self._lottie_obj['layers'].insert(layer_index, new_layer.layer)

    def find_main_layer(self, layer_id: int = None, layer_name: str = None):
        find_layer(self._layers, layer_id, layer_name)

    def delete_main_layer(self, layer_id: int, layer_name: str = None):
        layer_index = delete_layer(self.layers, layer_id, layer_name)
        if layer_index is not None:
            self._lottie_obj['layers'].remove(self.layers[layer_index].layer)

    def replace_main_layer(self, new_layer: Layer, layer_id=None, layer_name: str = None):
        layer_index = replace_layer(self.layers, new_layer, layer_id, layer_name)
        if layer_index is not None:
            self._lottie_obj['layers'][layer_index] = new_layer.layer

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

    @property
    def metadata(self):
        if 'meta' in self._lottie_obj:
            return self._lottie_obj['meta']
        else:
            return None

    @metadata.setter
    def metadata(self, metadata):
        self._lottie_obj['meta'] = metadata
