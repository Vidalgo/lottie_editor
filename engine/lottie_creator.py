from pathlib import Path
import copy

from engine.layer import Layer, Lottie_layer_type
from engine.lottie_animation import Lottie_animation
from engine.precomposition import Precomposition
from engine.vidalgo_lottie_base import Vidalgo_lottie_base
from engine.transform import Transform

PATH = Path(__file__).parents[1].joinpath('tests')
INPUT_PATH = PATH.joinpath('inputs')
OUTPUT_PATH = PATH.joinpath('outputs')


class Lottie_creator:
    def __init__(self, lottie_obj: Lottie_animation, source_lottie_objects_uuids: list[str]):
        self._lottie_obj = lottie_obj
        self._new_lottie_obj = Lottie_animation()
        # Source list holds layers that act as source nodes for compositions
        # destination lists hold objects (layers, images, precomp) that will generate the new composition
        self._source_lottie_objects_uuids = source_lottie_objects_uuids
        self._destination_layers: dict = {}
        self._destination_images: dict = {}
        self._destination_precomp: dict = {}
        # self._destination_lottie_objects_uuids: list = []
        # create a layers dictionary. Each layer points to its composition (for fast access)
        self._layers_to_compositions: dict = {}
        for precomp in lottie_obj.precomposition:
            for layer in precomp.layers:
                self._layers_to_compositions[layer.vidalgo_id] = precomp.vidalgo_id
        # if layer in main layer create a dedicated id
        for layer in lottie_obj.layers:
            self._layers_to_compositions[layer.vidalgo_id] = "zlottie_layers"
        # create a precomposition dictionary. Each precomposition points to its precomposition layer (for fast access)
        self._compositions_to_layers: dict = {}

    @property
    def original_lottie(self):
        return self._lottie_obj

    @property
    def derived_lottie(self):
        return self._new_lottie_obj

    def create(self, filename: str):
        self._find_source_layers_compositions()
        self._new_lottie_obj = copy.deepcopy(self._lottie_obj)
        self._remove_redundant_images()
        self._remove_redundant_layers()
        self._remove_redundant_precomp()
        self._remove_redundant_main_layers()
        #self._new_lottie_obj.name = '{0}_derivative_{1}'.format(self._lottie_obj.name, Vidalgo_lottie_base.uuid(2)) \
#            if filename is None else filename
        output_file_name = str(OUTPUT_PATH.joinpath(f'{self._new_lottie_obj.name}.json'))
        self._new_lottie_obj.add_lottie_id(refactor_ids=True)
        self._new_lottie_obj.store(output_file_name)

    def _find_source_layers_compositions(self):
        all_lottie_elements_dict = Vidalgo_lottie_base.vidalgo_lottie_elements
        for source_uuid in self._source_lottie_objects_uuids:
            if not isinstance(all_lottie_elements_dict[source_uuid], Layer):
                raise ValueError("uuid {0} is not a layer", source_uuid)
            # add the source layer as a root node of the trees
            '''if source_uuid not in self._destination_lottie_objects_uuids:
                self._destination_lottie_objects_uuids.append(source_uuid)'''
            self._destination_layers[source_uuid] = all_lottie_elements_dict[source_uuid]
            # add the precomposition that contain the source layers to destination and to the composition dic as
            # a composition without a reference
            '''if self._layers_to_compositions_uuid[source_uuid] not in self._destination_lottie_objects_uuids:
                self._destination_lottie_objects_uuids.append(self._layers_to_compositions_uuid[source_uuid])'''
            if self._layers_to_compositions[source_uuid] != "zlottie_layers":
                self._destination_precomp[self._layers_to_compositions[source_uuid]] = \
                    all_lottie_elements_dict[self._layers_to_compositions[source_uuid]]

            self._compositions_to_layers[self._layers_to_compositions[source_uuid]] = False

            self._append_children_uuids(source_uuid)
            self._append_image_uuid(source_uuid)
            self._append_precomp_uuids(source_uuid)

    def _append_children_uuids(self, source_uuid: str):
        all_lottie_elements_dict = Vidalgo_lottie_base.vidalgo_lottie_elements
        layer_id = all_lottie_elements_dict[source_uuid].id
        # Traverse all layers in the same precomposition as the source
        for child_layer_uuid in self._layers_to_compositions:
            if self._layers_to_compositions[child_layer_uuid] == self._layers_to_compositions[source_uuid]:
                # find the layers in which the source is their parent
                parent_id = all_lottie_elements_dict[child_layer_uuid].parent
                if parent_id is not None and parent_id == layer_id:
                    # store layer uuid both in source (to test it later) and destination
                    '''if child_layer_uuid not in self._destination_lottie_objects_uuids:
                        self._destination_lottie_objects_uuids.append(child_layer_uuid)'''
                    self._destination_layers[child_layer_uuid] = all_lottie_elements_dict[child_layer_uuid]
                    if child_layer_uuid not in self._source_lottie_objects_uuids:
                        self._source_lottie_objects_uuids.append(child_layer_uuid)

    def _append_image_uuid(self, source_uuid: str):
        all_lottie_elements_dict = Vidalgo_lottie_base.vidalgo_lottie_elements
        layer = all_lottie_elements_dict[source_uuid]
        # handle image references only - find the image and store its uuid in destination
        if layer.type == Lottie_layer_type.Image.value:
            image_uuid = [image.vidalgo_id for image in self._lottie_obj.images if image.id == layer.reference_id][0]
            '''if image_uuid not in self._destination_lottie_objects_uuids:
                self._destination_lottie_objects_uuids.append(image_uuid)'''
            self._destination_images[image_uuid] = all_lottie_elements_dict[image_uuid]

    def _append_precomp_uuids(self, source_uuid: str):
        all_lottie_elements_dict = Vidalgo_lottie_base.vidalgo_lottie_elements
        layer = all_lottie_elements_dict[source_uuid]
        # handle precomp references only
        if layer.type == Lottie_layer_type.Precomp.value:
            # find the precomposition referenced by the precomp layer
            precomp = [precomp for precomp in self._lottie_obj.precomposition if precomp.id == layer.reference_id][0]
            # store the precomposition in destination and mark it in the dedicated precomposition dict
            # Store all its internal layers in source to be handled later
            '''if len(precomp) != 0 and precomp.vidalgo_id not in self._destination_lottie_objects_uuids:
                self._destination_lottie_objects_uuids.append(precomp.vidalgo_id)'''
            self._destination_precomp[precomp.vidalgo_id] = all_lottie_elements_dict[precomp.vidalgo_id]
            self._compositions_to_layers[precomp.lottie_element_id] = True
            [self._source_lottie_objects_uuids.append(layer.vidalgo_id) for layer in precomp.layers
             if layer.vidalgo_id not in self._source_lottie_objects_uuids]

    def _remove_redundant_images(self):
        [self._new_lottie_obj.images.remove(image) for image in self._new_lottie_obj.images
         if image.lottie_element_id not in self._destination_images]

    def _remove_redundant_layers(self):
        [self._new_lottie_obj.precomposition.remove(layer) for layer in
         [precomp for precomp in self._new_lottie_obj.precomposition]
         if layer.lottie_element_id not in self._destination_layers]

        '''for precomp in self._new_lottie_obj.precomposition:
            for layer in precomp:
                if layer.lottie_element_id not in self._destination_layers:
                    self._new_lottie_obj.precomposition.remove(layer)'''

    def _remove_redundant_precomp(self):
        [self._new_lottie_obj.precomposition.remove(precomp) for precomp in self._new_lottie_obj.precomposition
         if precomp.lottie_element_id not in self._destination_precomp]

    def _remove_redundant_main_layers(self):
        [self._new_lottie_obj.layers.remove(layer) for layer in self._new_lottie_obj.layers
         if layer.lottie_element_id not in self._destination_layers]

    def _add_main_precomp_layers(self):
        # go over all remaining precompositions and add precomposition layers to the ones without a reference
        # need to locate the original precomp layer and make it a main layer
        for precomp_uuid in self._destination_precomp:
            if not self._compositions_to_layers[precomp_uuid]:
                for precomp_layer_uuid in self._layers_to_compositions:
                    precomp_layer = self._layers_to_compositions[precomp_layer_uuid]
                    if type(precomp_layer) is Precomposition and precomp_layer.reference_id == precomp_uuid:
                        precomp_layer.parent = None
                        precomp_layer.set_zlottie_id()
                        precomp_layer.transform = Transform()
                        if precomp_layer.width is not None and precomp_layer.width is not None:
                            [width, height] = [precomp_layer.width / 2, precomp_layer.height / 2]
                        else:
                            [width, height] = [self._new_lottie_obj.width / 2, self._new_lottie_obj.height / 2]
                        precomp_layer.transform.anchor = [width, height]
                        precomp_layer.transform.position = [width, height]
                        self._new_lottie_obj.add_layer(precomp_layer)
