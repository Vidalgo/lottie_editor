from __future__ import annotations

import random
from os import makedirs, path

from vidalgo_lottie_base import Vidalgo_lottie_base, ID_SUFFIX, PATH
from helpers import update_intersected_ids, store_json

from metadata import Metadata
from font import Font
from char import Char
from image_asset import Image_asset
from precomposition import Precomposition
from layer import Layer, Lottie_layer_type, find_layer, add_layer, delete_layer, replace_layer, update_ref_id
from precomp_layer import Precomp_layer
from text_layer import Text_layer, refactor_font_name


class Lottie_animation(Vidalgo_lottie_base):
    def __init__(self, lottie_name: str = 'unknown', in_point: int = 0, out_point: int = 30, frame_rate: int = 30,
                 ddd_layers: int = 0, width: float = 500, height: float = 500, version: str = "5.5.2"):
        super(Lottie_animation, self).__init__()
        self._main_layers_index = 0
        self._refactor_animation_ids: bool = False
        # self._null_layer_id_counter = 1000
        # self._pre_comb_id_counter = 10
        self._metadata = None
        self._main_layer: Layer = None
        self._main_precomposition: Precomposition = None
        self._fonts: list[Font] = []
        self._chars: list[Char] = []
        self._layers: list[Layer] = []
        self._images: list[Image_asset] = []
        self._precomposition: list[Precomposition] = []
        self._create_vidalgo_lottie_template(lottie_name, in_point, out_point, frame_rate, ddd_layers, width, height,
                                             version)

    def _create_vidalgo_lottie_template(self, lottie_name: str = 'vidalgo_lottie', in_point: int = 0, out_point: int = 30,
                                        frame_rate: int = 30, ddd_layers: int = 0, width: float = 500,
                                        height: float = 500, version: str = "5.5.2"):
        self.version = version
        self.name = lottie_name
        self.width = width
        self.height = height
        self.frame_rate = frame_rate
        self.in_point = in_point
        self.out_point = out_point
        self.ddd_layers = ddd_layers
        self.assets = []
        self._create_vidalgo_lottie_main_precomposition('{0}_main_precomposition'.format(lottie_name), frame_rate)
        self._create_vidalgo_lottie_main_layer('{0}_main_layer'.format(lottie_name), width, height)

    def _create_vidalgo_lottie_main_layer(self, name: str, width: float, height: float):
        main_precomposition_ref_id = self.main_precomposition.id if self.main_precomposition.id is not None else ''
        main_layer_name = '{0}_{1}'.format(name, self.uuid(4))
        self._main_layer = Precomp_layer(self.main_layers_index, main_layer_name, layer_transform=True,
                                         reference_id=main_precomposition_ref_id, width=width, height=height)
        self._main_layer.out_point = self.out_point
        self.layers.append(self._main_layer)
        self.lottie_base['layers'] = [self._main_layer.layer]

    def _create_vidalgo_lottie_main_precomposition(self, name: str, frame_rate: int):
        self._main_precomposition = Precomposition(name, name, frame_rate)
        self.add_precomposition(self.main_precomposition, add_uuid_and_refactor=False)

    def _refactor_ids(self):
        self._main_layers_index = 0
        layers_ids_dictionary = {}
        pre_comp_ids_dictionary = {}
        images_comp_ids_dictionary = {}
        for layer in self.layers:
            index = self.main_layers_index
            layers_ids_dictionary[layer.id] = index
            layer.id = index
        for asset in self.assets:
            refactored_id = "{0}_{1}".format(asset['id'], str(self.main_layers_index))
            if 'id' in asset:
                pre_comp_ids_dictionary[asset['id']] = refactored_id
            elif 'e' in asset:
                images_comp_ids_dictionary[asset['id']] = refactored_id
            asset['id'] = refactored_id
        for layer in self.layers:
            if layer.parent is not None:
                layer.parent = layers_ids_dictionary[layer.parent]
            if layer.reference_id is not None:
                if layer.reference_id in pre_comp_ids_dictionary:
                    layer.reference_id = pre_comp_ids_dictionary[layer.reference_id]
                else:
                    layer.reference_id = images_comp_ids_dictionary[layer.reference_id]

    @staticmethod
    def _refactor_ref_id(layer: Layer, element_ids_with_uuid: list[str]):
        for element_id_with_uuid in element_ids_with_uuid:
            element_id = Vidalgo_lottie_base.remove_uuid(element_id_with_uuid)
            if layer.reference_id == element_id:
                layer.reference_id = element_id_with_uuid

    def _refactor_layers_ref_id(self, element_ids_with_uuid: list[str] = None):
        element_ids_with_uuid = [pre_comp.refactor_id() for pre_comp in self.precomposition] \
            if element_ids_with_uuid is None else element_ids_with_uuid
        [self._refactor_ref_id(layer, element_ids_with_uuid) for precomp in self.precomposition for layer in precomp.layers
         if layer.type == Lottie_layer_type.Precomp.value]
        [self._refactor_ref_id(layer, element_ids_with_uuid) for layer in self.layers
         if layer.type == Lottie_layer_type.Precomp.value]

    def _refactor_image_ref_id(self, element_ids_with_uuid: list[str] = None):
        element_ids_with_uuid = [image.refactor_id() for image in self.images] if element_ids_with_uuid is None \
            else element_ids_with_uuid
        [self._refactor_ref_id(layer, element_ids_with_uuid) for precomp in self.precomposition for layer in precomp.layers
         if layer.type == Lottie_layer_type.Image.value]
        [self._refactor_ref_id(layer, element_ids_with_uuid) for layer in self.layers
         if layer.type == Lottie_layer_type.Image.value]

    def _refactor_font_ref_id(self):
        element_ids_with_uuid = [font.refactor_id() for font in self.fonts]
        [refactor_font_name(layer, element_ids_with_uuid) for precomp in self.precomposition for layer in precomp.layers
         if layer.type == Lottie_layer_type.Text.value]
        [refactor_font_name(layer, element_ids_with_uuid) for layer in self.layers
         if layer.type == Lottie_layer_type.Text.value]

    def _refactor_char_ref_id(self):
        def _refactor_font_family(font: Font):
            font.font_family = char.font_family
        chars_uuids = {}
        for char in self.chars:
            font_family = char.font_family
            if font_family in chars_uuids:
                uuid = chars_uuids[char.font_family]
            else:
                uuid = self.uuid(4)
                chars_uuids[char.font_family] = uuid
            char.font_family = '{0}_{1}'.format(font_family, uuid)
            [_refactor_font_family(font) for font in self.fonts if font.font_family == font_family]

    def _refactor_references(self, refactor_fonts_and_chars=False):
        if refactor_fonts_and_chars:
            self._refactor_char_ref_id()
            self._refactor_font_ref_id()
        self._refactor_image_ref_id()
        self._refactor_layers_ref_id()

    '''def _update_ref_id(self, layer_type: Lottie_layer_type, ref_id: str, updated_ref_id: str):
        for pre_comp in self.precomp:
            update_ref_id(pre_comp.layers, layer_type, ref_id, updated_ref_id)
        update_ref_id(self.layers, layer_type, ref_id, updated_ref_id)'''

    '''def _adjust_precompositions_intersection(self, animation: Lottie_animation):
        precomp_id_intersections = update_intersected_ids(animation.precomp, self.precomp)
        if precomp_id_intersections is not None:
            for precomp_id in precomp_id_intersections:
                self._update_ref_id(Lottie_layer_type.Precomp, precomp_id, '{0}{1}'.format(precomp_id, ID_SUFFIX))'''

    '''def _adjust_images_intersection(self, animation: Lottie_animation):
        image_id_intersections = update_intersected_ids(animation.images, self.images)
        if image_id_intersections is not None:
            for image_id in image_id_intersections:
                self._update_ref_id(Lottie_layer_type.Image, image_id, '{0}{1}'.format(image_id, ID_SUFFIX)) '''

    '''def _adjust_fonts_intersection(self, animation: Lottie_animation):
        font_id_intersections = update_intersected_ids(animation.fonts, self.images)
        if font_id_intersections is not None:
            for font_id in font_id_intersections:
                self._update_ref_id(Lottie_layer_type.Text, font_id, '{0}{1}'.format(font_id, ID_SUFFIX))'''

    def __add__(self, animation: Lottie_animation):
        def _adjust_animation_main_layers():
            for layer_id, layer in enumerate(animation.layers):
                transform_pos = [(random.random() - .5) * self.width, (random.random() - .5) * self.height]
                layer.id = layer_id + self.main_layers_index
                layer.transform.position = transform_pos
            self.layers += animation.layers
        # markers : no check needed
        # motion blur : use destination but issue a warning if source motion blur exists
        self.in_point = min(self.in_point, animation.in_point)
        self.out_point = max(self.out_point, animation.out_point)
        # self.width += animation.width
        # self.height += animation.height
        self.width = max(self.width, animation.width)
        self.height = max(self.height, animation.height)
        self.ddd_layers = max(self.ddd_layers, animation.ddd_layers)
        self.assets += animation.assets
        self.fonts += animation.fonts
        self.chars += animation.chars
        self.precomposition += animation.precomposition
        self.images += animation.images
        _adjust_animation_main_layers()
        # self.markers += animation.markers
        return self

    def load(self, animation_file_name, refactor_fonts_and_chars=False):
        def _load_metadata(metadata: dict):
            new_metadata = Metadata()
            new_metadata.load(metadata)
            return new_metadata

        def _load_font(font: dict):
            new_font = Font()
            new_font.load(font)
            return new_font

        def _load_char(char: dict):
            new_char = Char()
            new_char.load(char)
            return new_char

        def _load_layer(layer: dict, lottie_base: dict):
            layer_type = '{0}_layer'.format(Lottie_layer_type(Layer.get_type(layer)).name)
            new_layer = globals()[layer_type]() if layer_type in globals() else Layer()
            new_layer.load(layer)
            return new_layer

        def _load_asset():
            if 'assets' in self.lottie_base and self.lottie_base['assets'] is not None:
                for asset in self.lottie_base['assets']:
                    if 'e' in asset:
                        new_asset = Image_asset()
                        new_asset.load(asset)
                        self._images.append(new_asset)
                    else:
                        new_asset = Precomposition()
                        new_asset.load(asset)
                        self._precomposition.append(new_asset)

        super(Lottie_animation, self).load(animation_file_name)
        self.analyze()
        self._precomposition = []
        self._layers = []
        self._main_layers_index = 0
        refactor_animation = False if self.vidalgo_lottie else True
        self._fonts = [] if 'fonts' not in self.lottie_base or 'list' not in self.lottie_base['fonts'] else\
            [_load_font(font) for font in self.lottie_base['fonts']['list']]
        self._chars = [] if 'chars' not in self.lottie_base else \
            [_load_char(char) for char in self.lottie_base['chars']]
        self._layers = [_load_layer(layer, self.lottie_base) for layer in self.lottie_base['layers']]
        _load_asset()
        # self._markers = self.main
        self._metadata = _load_metadata(self.lottie_base['meta']) if 'meta' in self.lottie_base else None
        if refactor_animation:
            self._refactor_references(refactor_fonts_and_chars)
            self._create_vidalgo_lottie_main_precomposition('{0}_main_precomp'.format(self.name), self.frame_rate)
            self.main_precomposition.layers = self.layers
            self.layers = []
            self._create_vidalgo_lottie_main_layer('{0}_main_layer'.format(self.name), self.width, self.height)

    def store(self, file_name=None):
        if file_name is None:
            if not path.isdir(PATH):
                makedirs(PATH)
            file_name = "{0}{1}.json".format(PATH, self.name)
        self.metadata = Metadata()
        store_json(file_name, self.lottie_base)

    def copy(self, animation: dict):
        super(Lottie_animation, self).copy(animation)
        self.analyze()

    def analyze(self):
        super(Lottie_animation, self).analyze()
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
    def main_layers_index(self):
        index = self._main_layers_index
        self._main_layers_index += 1
        return index

    @property
    def lottie(self):
        return self.lottie_base

    @lottie.setter
    def lottie(self, lottie: dict):
        self.lottie_base = lottie
        self.analyze()

    @property
    def main_layer(self):
        return self._main_layer

    @property
    def main_precomposition(self):
        return self._main_precomposition

    @property
    def name(self):
        if 'nm' in self.lottie_base:
            return self.lottie_base['nm']
        else:
            return None

    @name.setter
    def name(self, name: str):
        self.lottie_base['nm'] = name

    @property
    def version(self):
        if 'v' in self.lottie_base:
            return self.lottie_base['v']
        else:
            return None

    @version.setter
    def version(self, version: str):
        self.lottie_base['v'] = version

    @property
    def match_name(self):
        if 'mn' in self.lottie_base:
            return self.lottie_base['mn']
        else:
            return None

    @match_name.setter
    def match_name(self, match_name: str):
        self.lottie_base['mn'] = match_name

    @property
    def in_point(self):
        if 'ip' in self.lottie_base:
            return self.lottie_base['ip']
        else:
            return None

    @in_point.setter
    def in_point(self, in_point: int):
        self.lottie_base['ip'] = in_point

    @property
    def out_point(self):
        if 'op' in self.lottie_base:
            return self.lottie_base['op']
        else:
            return None

    @out_point.setter
    def out_point(self, out_point: int):
        self.lottie_base['op'] = out_point

    @property
    def frame_rate(self):
        if 'fr' in self.lottie_base:
            return self.lottie_base['fr']
        else:
            return None

    @frame_rate.setter
    def frame_rate(self, frame_rate: int):
        self.lottie_base['fr'] = frame_rate

    @property
    def ddd_layers(self):
        if 'ddd' in self.lottie_base:
            return self.lottie_base['ddd']
        else:
            return None

    @ddd_layers.setter
    def ddd_layers(self, ddd_layers: int):
        self.lottie_base['ddd'] = ddd_layers

    @property
    def width(self):
        if 'w' in self.lottie_base:
            return self.lottie_base['w']
        else:
            return None

    @width.setter
    def width(self, width: float):
        self.lottie_base['w'] = width

    @property
    def height(self):
        if 'h' in self.lottie_base:
            return self.lottie_base['h']
        else:
            return None

    @height.setter
    def height(self, height: float):
        self.lottie_base['h'] = height

    @property
    def bodymovin_version(self):
        if 'v' in self.lottie_base:
            return self.lottie_base['v']
        else:
            return None

    @bodymovin_version.setter
    def bodymovin_version(self, bodymovin_version: str):
        self.lottie_base['v'] = bodymovin_version

    @property
    def fonts(self):
        return self._fonts

    @fonts.setter
    def fonts(self, fonts: list[Font]):
        self._fonts = fonts
        if 'font' not in self.lottie_base:
            self.lottie_base['fonts'] = {}
        self.lottie_base['fonts']['list'] = [font.font for font in fonts]

    def add_font(self, font: Font):
        if 'fonts' not in self.lottie_base:
            self.lottie_base['fonts'] = {'list': []}
        else:
            for fonts in self.fonts:
                if fonts.font_name == font.font_name:
                    return
        self.fonts.insert(0, font)
        self.lottie_base['fonts']['list'].insert(0, font.font)

    def find_font(self, font_name: str):
        for font in self.fonts:
            if font.font_name == font_name:
                return font
        return None

    def delete_font(self, font_name: str):
        font = self.find_font(font_name)
        if font is not None:
            self.fonts.remove(font)
            self.lottie_base['fonts']['list'].remove(font.font)

    def replace_font(self, new_font: Font, replaced_font_name):
        for index, font in enumerate(self.fonts):
            if font.font_name == replaced_font_name:
                self.fonts[index] = new_font
                self.lottie_base['fonts']['list'][index] = new_font.font
                update_font_name(self.layers, replaced_font_name, new_font.font_name)
                for precomp_ref in self.precomposition:
                    update_font_name(precomp_ref.layers, replaced_font_name, new_font.font_name)
                break

    @property
    def chars(self):
        return self._chars

    @chars.setter
    def chars(self, chars: list[Char]):
        self._chars = chars
        if 'chars' not in self.lottie_base:
            self.lottie_base['chars'] = {}
        self.lottie_base['chars'] = [char.char for char in chars]

    def add_char(self, char: Char):
        if 'chars' not in self.lottie_base:
            self.lottie_base['chars'] = None
        else:
            for chars in self.chars:
                if chars.character == char.character:
                    return
        self.chars.insert(0, char)
        self.lottie_base['chars'].insert(0, char.char)

    def find_char(self, char_name: str):
        for char in self.chars:
            if char.character == char_name:
                return char
        return None

    def delete_char(self, char_name: str):
        char = self.find_char(char_name)
        if char is not None:
            self.chars.remove(char)
            self.lottie_base['chars'].remove(char.character)

    def replace_char(self, new_char: Char, replaced_char_name):
        for index, char in enumerate(self.chars):
            if char.character == replaced_char_name:
                self.chars[index] = new_char
                self.lottie_base['chars'][index] = new_char.character
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
        self.lottie_base['layers'] = [lottie_layer.layer for lottie_layer in lottie_layers]

    @property
    def assets(self):
        if 'assets' in self.lottie_base:
            return self.lottie_base['assets']
        else:
            return None

    @assets.setter
    def assets(self, assets: list):
        self.lottie_base['assets'] = assets

    @property
    def images(self):
        return self._images

    @images.setter
    def images(self, images: list[Image_asset], add_uuid=False):
        if add_uuid:
            for image in images:
                image.lottie_element_id = image.id
        self._images = images
        pre_comps_temp = [pre_comp.precomp for pre_comp in self.precomposition]
        self.lottie_base['assets'] = [image._lottie_obj for image in images] + pre_comps_temp

    def add_image(self, image: Image_asset, add_uuid_and_refactor=False):
        if add_uuid_and_refactor:
            image.lottie_element_id = image.id
            self._refactor_image_ref_id([image.lottie_element_id])
        self.images.insert(0, image)
        self.lottie_base['assets'].insert(0, image._lottie_obj)

    def find_image(self, image_id):
        for image in self.images:
            if image_id == self.remove_uuid(image.id):
                return image
        return None

    def delete_image(self, image_id):
        image = self.find_image(image_id)
        if image is not None:
            self.images.remove(image)
            self.lottie_base['assets'].remove(image.image)

    def replace_image(self, new_image: Image_asset, replaced_image_id):
        for index, image in enumerate(self.images):
            if replaced_image_id == self.remove_uuid(image.id):
                self.images[index] = new_image
                self.lottie_base['assets'][index] = new_image._lottie_obj
                self._refactor_image_ref_id([image.lottie_element_id])

    @property
    def precomposition(self):
        return self._precomposition

    @precomposition.setter
    def precomposition(self, precomps: list[Precomposition], add_uuid=False):
        if add_uuid:
            for precomp in precomps:
                precomp.lottie_element_id = precomp.id
        self._precomposition = precomps
        images_temp = [image.image for image in self.images]
        self.lottie_base['assets'] = images_temp + [precomp.precomp for precomp in precomps]

    def add_precomposition(self, precomp: Precomposition, add_uuid_and_refactor=True):
        if add_uuid_and_refactor:
            precomp.lottie_element_id = precomp.id
            self._refactor_layers_ref_id([precomp.lottie_element_id])
        self.precomposition.insert(0, precomp)
        self.lottie_base['assets'].append(precomp.precomp)

    def find_precomposition(self, precomb_id):
        for precomb in self.precomposition:
            if precomb_id == self.remove_uuid(precomb.id):
                return precomb
        return None

    def delete_precomposition(self, precomb_id):
        precomp = self.find_precomposition(precomb_id)
        if precomp is not None:
            self.precomposition.remove(precomp)
            self.lottie_base['assets'].remove(precomp.precomp)

    def replace_precomposition(self, new_precomp: Precomposition, replaced_precomp_id):
        for index, precomp in enumerate(self.precomposition):
            if replaced_precomp_id == self.remove_uuid(precomp.id):
                new_precomp.vidalgo_id = replaced_precomp_id
                self.precomposition[index] = new_precomp
                self.lottie_base['assets'][index] = new_precomp.precomp
                self._refactor_layers_ref_id([precomp.lottie_element_id])

    def add_layer(self, new_layer: Layer, update_layer_id=True, order='last', layer_id: int = None):
        self.main_precomposition.add_layer(new_layer, update_layer_id, order, layer_id)


    def find_main_layer(self, layer_id: int = None, layer_name: str = None):
        find_layer(self._layers, layer_id, layer_name)

    def delete_main_layer(self, layer_id: int, layer_name: str = None):
        layer_index = delete_layer(self.layers, layer_id, layer_name)
        if layer_index is not None:
            self.lottie_base['layers'].remove(self.layers[layer_index].layer)

    def replace_main_layer(self, new_layer: Layer, layer_id=None, layer_name: str = None):
        layer_index = replace_layer(self.layers, new_layer, layer_id, layer_name)
        if layer_index is not None:
            self.lottie_base['layers'][layer_index] = new_layer.layer

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
    def vidalgo_lottie(self):
        if self.metadata is not None and self.metadata.keywords is not None and len(self.metadata.keywords) > 0:
            return True if self.metadata.decrypt() == "vidalgo" else False
        return False

    @property
    def metadata(self):
        if 'meta' in self.lottie_base:
            return self._metadata
        else:
            return None

    @metadata.setter
    def metadata(self, metadata: Metadata):
        self._metadata = metadata
        self._lottie_obj['meta'] = metadata.metadata
