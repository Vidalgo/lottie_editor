from pathlib import Path
import copy

from engine.layer import Layer, Lottie_layer_type
from engine.lottie_animation import Lottie_animation
from engine.precomposition import Precomposition
from engine.vidalgo_lottie_base import Vidalgo_lottie_base
from engine.transform import Transform
from engine.precomp_layer import Precomp_layer

PATH = Path(__file__).parents[1].joinpath('tests')
INPUT_PATH = PATH.joinpath('inputs')
OUTPUT_PATH = PATH.joinpath('outputs')
MAIN_LAYERS = "zlottie_layers"


class Update_colors:
    class Color:
        def __init__(self, recolor=None):
            self._color = recolor

        def update(self, lottie_obj):
            if self._color is None or len(self._color) != 4:
                return
            try:
                if 'c' in lottie_obj and type(lottie_obj['c']) is dict and 'k' in lottie_obj['c'] and lottie_obj['c']['a'] == 0:
                    lottie_obj['c']['k'] = self._color
            except:
                print(lottie_obj)
                pass


    def __init__(self, uuids: list[str], hide=False, opacity=100, recolor=None):
        self._uuids = uuids
        self._hide = hide
        self._opacity = opacity
        self._color = recolor

    def update(self, lottie_obj):
        if 'ln' in lottie_obj and lottie_obj['ln'] in self._uuids:
            if lottie_obj is not None:
                lottie_obj['hd'] = self._hide
                if 'o' in lottie_obj and 'k' in lottie_obj['o'] and lottie_obj['o']['a'] == 0:
                    lottie_obj['o']['k'] = self._opacity
                if 'ks' in lottie_obj and 'o' in lottie_obj['ks'] and 'k' in lottie_obj['ks']['o'] and lottie_obj['ks']['o']['a'] == 0:
                    lottie_obj['ks']['o']['k'] = self._opacity
                Vidalgo_lottie_base.update_elements(lottie_obj, Update_colors.Color(self._color))


class Lottie_creator:
    def __init__(self, lottie_obj: Lottie_animation, source_lottie_objects_uuids: list[str]):
        self._lottie_obj = lottie_obj
        self._new_lottie_obj = Lottie_animation()
        # Source list holds layers that act as source nodes for compositions
        # destination lists hold objects (layers, images, precomp) that will generate the new composition
        self._source_lottie_objects_uuids = source_lottie_objects_uuids
        self._destination_layers: dict = {}
        self._destination_images: dict = {}
        #self._destination_precomp: dict = {}
        # create a layer dictionary. Each layer points to its composition (for fast access)
        self._layers_to_precompositions: dict = {}
        # create a precomposition dictionary. Each precomposition points to its precomposition layer (for fast access)
        self._precompositions_to_precomp_layers: dict = {}
        # create a layer dictionary. Each layer points to the precomp layer that points to the layer precomposition
        self._layers_to_precomp_layers: dict = {}
        # create a list of all precomposition layers that lead to the source layers
        self._precomp_layer_tree: list = []
        # create UUID dics: Layer->Precomp ; Precomp->Precomp_layer ; Layer->Precomp_layer
        self._set_layers_to_precomp_layers()

    @property
    def original_lottie(self):
        return self._lottie_obj

    @property
    def derived_lottie(self):
        return self._new_lottie_obj

    def mark_elements(self, name: str, hide=False, opacity=100, recolor=None):
        self._lottie_obj.name = name
        update_colors = Update_colors(self._source_lottie_objects_uuids, hide, opacity, recolor)
        Vidalgo_lottie_base.update_elements(self._lottie_obj.lottie_base, update_colors)
        output_file_name = str(OUTPUT_PATH.joinpath(f'{self._lottie_obj.name}.json'))
        self._lottie_obj.add_lottie_id(refactor_ids=False)
        self._lottie_obj.store(output_file_name)

    def hide(self, name: str):
        self._find_source_layers_compositions()
        self._find_precomp_layer_trees()
        self._hide_redundant_layers()
        self._lottie_obj.name = name
        output_file_name = str(OUTPUT_PATH.joinpath(f'{self._lottie_obj.name}.json'))
        self._lottie_obj.add_lottie_id(refactor_ids=True)
        self._lottie_obj.store(output_file_name)

    def create(self, name: str):
        self._find_source_layers_compositions()
        self._find_precomp_layer_trees()
        self._new_lottie_obj = copy.deepcopy(self._lottie_obj)
        self._remove_redundant_images()
        self._remove_redundant_layers()
        self._remove_redundant_precomp()
        #self._add_main_precomp_layers()
        self._new_lottie_obj.name = name
        output_file_name = str(OUTPUT_PATH.joinpath(f'{self._new_lottie_obj.name}.json'))
        self._new_lottie_obj.add_lottie_id(refactor_ids=False)
        self._new_lottie_obj.store(output_file_name)

    def _find_source_layers_compositions(self):
        all_lottie_elements_dict = Vidalgo_lottie_base.vidalgo_lottie_elements
        for source_uuid in self._source_lottie_objects_uuids:
            if not isinstance(all_lottie_elements_dict[source_uuid], Layer):
                raise ValueError("uuid {0} is not a layer", source_uuid)
            # add the source layer as a root node of the trees
            self._destination_layers[source_uuid] = all_lottie_elements_dict[source_uuid]
            self._append_children_uuids(source_uuid)
            self._append_precomp_uuids(source_uuid)
            self._append_image_uuid(source_uuid)

    def _append_children_uuids(self, source_uuid: str):
        all_lottie_elements_dict = Vidalgo_lottie_base.vidalgo_lottie_elements
        layer_id = all_lottie_elements_dict[source_uuid].id
        # Traverse all layers in the same precomposition as the source
        for child_layer_uuid in self._layers_to_precompositions:
            if self._layers_to_precompositions[child_layer_uuid] == self._layers_to_precompositions[source_uuid]:
                # find the layers in which the source is their parent
                parent_id = all_lottie_elements_dict[child_layer_uuid].parent
                if parent_id is not None and parent_id == layer_id:
                    # store layer uuid both in source (to test it later) and destination
                    self._destination_layers[child_layer_uuid] = all_lottie_elements_dict[child_layer_uuid]
                    if child_layer_uuid not in self._source_lottie_objects_uuids:
                        self._source_lottie_objects_uuids.append(child_layer_uuid)

    def _append_precomp_uuids(self, source_uuid: str):
        all_lottie_elements_dict = Vidalgo_lottie_base.vidalgo_lottie_elements
        layer = all_lottie_elements_dict[source_uuid]
        # handle precomp references only
        if layer.type == Lottie_layer_type.Precomp.value:
            # find the precomposition referenced by the precomp layer
            precomp = [precomp for precomp in self._lottie_obj.precomposition if precomp.id == layer.reference_id][0]
            # Store all its internal layers in source to be handled later
            [self._source_lottie_objects_uuids.append(layer.vidalgo_id) for layer in precomp.layers
             if layer.vidalgo_id not in self._source_lottie_objects_uuids]

    def _append_image_uuid(self, source_uuid: str):
        all_lottie_elements_dict = Vidalgo_lottie_base.vidalgo_lottie_elements
        layer = all_lottie_elements_dict[source_uuid]
        # handle image references only - find the image and store its uuid in destination
        if layer.type == Lottie_layer_type.Image.value:
            image_uuid = [image.vidalgo_id for image in self._lottie_obj.images if image.id == layer.reference_id][0]
            self._destination_images[image_uuid] = all_lottie_elements_dict[image_uuid]

    def _set_layers_to_precomp_layers(self):
        def set_l_to_p(cls, l, p, t_precomp_to_precomp_layers) -> dict:
            cls._layers_to_precompositions[l.vidalgo_id] = p.vidalgo_id
            if l.type == Lottie_layer_type.Precomp.value:
                t_precomp_to_precomp_layers[l.reference_id] = l.vidalgo_id
            return {}

        def set_p_to_pl(cls, p, temp_precompositions_to_precomp_layers):
            cls._precompositions_to_precomp_layers[p.vidalgo_id] = \
                temp_precompositions_to_precomp_layers[p.id]

        def set_l_to_pl(cls, l):
            precomp_uuid = cls._layers_to_precompositions[l.vidalgo_id]
            precomp_layer_uuid = cls._precompositions_to_precomp_layers[precomp_uuid]
            cls._layers_to_precomp_layers[l.vidalgo_id] = precomp_layer_uuid

        t_precomp_to_precomp_layers = {}
        for layer in self._lottie_obj.layers:
            self._layers_to_precompositions[layer.vidalgo_id] = MAIN_LAYERS
            if layer.type == Lottie_layer_type.Precomp.value:
                t_precomp_to_precomp_layers[layer.reference_id] = layer.vidalgo_id

        [set_l_to_p(self, layer, precomp, t_precomp_to_precomp_layers) for precomp in self._lottie_obj.precomposition
         for layer in precomp.layers]

        [set_p_to_pl(self, precomp, t_precomp_to_precomp_layers) for precomp in self._lottie_obj.precomposition]

        [set_l_to_pl(self, layer) for precomp in self._lottie_obj.precomposition for layer in precomp.layers]

    def _find_precomp_layer_trees(self):
        def _find_next_precomp(layer_uuid: str):
            if layer_uuid in self._layers_to_precomp_layers:
                precomp_layer_uuid = self._layers_to_precomp_layers[layer_uuid]
            else:
                return
            if precomp_layer_uuid not in self._precomp_layer_tree:
                self._precomp_layer_tree.append(precomp_layer_uuid)
                _find_next_precomp(precomp_layer_uuid)
            else:
                return
        [_find_next_precomp(source_layer_uuid) for source_layer_uuid in self._source_lottie_objects_uuids]

    def _hide_redundant_layers(self):
        [layer.hide() for layer in self._lottie_obj.layers if layer.vidalgo_id not in self._destination_layers
         and layer.vidalgo_id not in self._precomp_layer_tree]
        [layer.hide() for precomp in self._lottie_obj.precomposition for layer in precomp.layers
         if layer.vidalgo_id not in self._destination_layers and layer.vidalgo_id not in self._precomp_layer_tree]

    def _remove_redundant_images(self):
        image_ids = {image.vidalgo_id: image.id for image in self._new_lottie_obj.images}
        for image_id in image_ids:
            if image_id not in self._destination_images:
                self._new_lottie_obj.delete_image(image_id)

    def _remove_redundant_layers(self):
        ids = {layer.vidalgo_id: layer.id for layer in self._new_lottie_obj.layers}
        [self._new_lottie_obj.delete_main_layer(layer_id) for vidalgo_id, layer_id in ids.items()
         if vidalgo_id not in self._destination_layers and vidalgo_id not in self._precomp_layer_tree]
        for precomp in self._new_lottie_obj.precomposition:
            ids = {layer.vidalgo_id: layer.id for layer in precomp.layers}
            for vidalgo_id, layer_id in ids.items():
                if vidalgo_id not in self._destination_layers and vidalgo_id not in self._precomp_layer_tree:
                    precomp.delete_layer(layer_id)

    def _remove_redundant_precomp(self):
        precomp_ids = []
        for precomp in self._new_lottie_obj.precomposition:
            if not precomp.layers:
                precomp_ids.append(precomp.id)
        [self._new_lottie_obj.delete_precomposition(precomp_id) for precomp_id in precomp_ids]


    def _add_main_precomp_layers(self):
        all_lottie_elements_dict = Vidalgo_lottie_base.vidalgo_lottie_elements
        # go over all remaining precompositions and add precomposition layers to the ones without a reference
        # need to locate the original precomp layer and make it a main layer
        for precomp_uuid in self._destination_precomp:
            if not self._compositions_to_layers[precomp_uuid]:
                precomp_id = self._destination_precomp[precomp_uuid].id
                for precomp_layer_uuid in self._layers_to_precompositions:
                    precomp_layer = all_lottie_elements_dict[precomp_layer_uuid]
                    if precomp_layer.type == Lottie_layer_type.Precomp.value and precomp_layer.reference_id == precomp_id:
                        precomp_layer.__class__ = Precomp_layer
                        precomp_layer.parent = None
                        precomp_layer.set_zlottie_id()
                        precomp_layer.transform = Transform()
                        if precomp_layer.width is not None and precomp_layer.height is not None:
                            [width, height] = [precomp_layer.width / 2, precomp_layer.height / 2]
                        else:
                            [width, height] = [self._new_lottie_obj.width / 2, self._new_lottie_obj.height / 2]
                        precomp_layer.transform.anchor = [width, height]
                        precomp_layer.transform.position = [width, height]
                        self._new_lottie_obj.add_layer(precomp_layer)
