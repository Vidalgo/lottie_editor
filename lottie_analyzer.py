from lottie_main import Lottie_main
from precomp import Precomp
from image import Image
from layer import Layer

from anytree import NodeMixin, Node, RenderTree
from anytree.exporter import DotExporter
from anytree.exporter import JsonExporter

import lottie_search_and_replace as lsr
from lottie_parser import Lottie_parser
from os import stat

from lottie_nlp import Lottie_nlp

RESTRICTED_NAMES_IN_LOTTIE = ["layer", "shape", "image", "comp", "group", "path", "fill"]

class Lottie_node(NodeMixin):
    def __init__(self, id, layer_type, name=None, composition_name=None, is_animated=False, parent_id=None,
                 lottie_obj=None, parent=None, reference_id=None, children=None, point_to_lottie_obj=False):
        self.id = id
        self.layer_type = layer_type
        self.name = name
        self.composition_name = composition_name
        self.is_animated = is_animated
        self.parent_id = parent_id
        self.lottie_obj = None
        self.parent = parent
        self.reference_id = reference_id
        if point_to_lottie_obj:
            self.lottie_obj = lottie_obj
        if children:
            self.children = children


class Lottie_analyzer(Lottie_parser):
    def __init__(self, lottie_filename):
        try:
            self.nodes = []
            Lottie_parser.__init__(self, lottie_filename)
            self.parse()
            self.lottie_file_size = 0
            self.number_of_frames = 0
            self.number_of_images = 0
            self.number_of_pre_comp = 0
            self.number_of_main_layers = 0
            self.errors_counter = {"errors": 0, "warnings": 0, "notices": 0}
            self.lottie_nlp_obj = Lottie_nlp()
            self.errors_and_warnings = {}
            self.point_to_lottie_obj = None
        except:
            raise Exception(f"Error:could not open JSON file {lottie_filename}")

    def set_error_or_warning(self, severity: str, message: str, layer_type: str, composition_name: str):
        message = f'{severity}: {message}' \
                  f' type "{layer_type}"' \
                  f' in composition "{composition_name}".'
        error_key = f'{severity}_{str(self.errors_counter)}'
        self.errors_and_warnings[error_key] = message
        if severity == 'Error':
            self.errors_counter["errors"] += 1
        elif severity == 'Warning':
            self.errors_counter["warnings"] += 1
        elif severity == 'Notice':
            self.errors_counter["notices"] += 1

    def eval_name(self, obj, obj_type, composition_name):
        layer_name = self.lottie_nlp_obj.to_lower(obj.name)
        if self.lottie_nlp_obj.all_numbers(layer_name):
            self.set_error_or_warning('Warning', f'name "{layer_name}" is all numbers.',
                                      obj_type, composition_name)
        elif self.lottie_nlp_obj.contains_number(layer_name):
            self.set_error_or_warning('Warning', f'name "{layer_name}" should not contain numbers.',
                                      obj_type, composition_name)
        for words in self.lottie_nlp_obj.tokenize(layer_name):
            if not self.lottie_nlp_obj.all_letters(words[0]):
                self.set_error_or_warning('Warning', f'word "{words[0]}" in name should contain letters.'
                                                            f'only',
                                          obj_type, composition_name)
            elif not self.lottie_nlp_obj.is_in_english(words[0]):
                self.set_error_or_warning('Warning', f'word "{words[0]}" in name not in English.',
                                          obj_type, composition_name)

        for restricted in RESTRICTED_NAMES_IN_LOTTIE:
            if Lottie_nlp.contains_sub_string(layer_name, restricted):
                self.set_error_or_warning('Notice', f'Avoid using "{restricted}" in name.',
                                          obj_type, composition_name)

    def test_layer_for_errors_and_warnings(self, layer: Layer, composition_name):
        if layer.name is None:
            self.set_error_or_warning('Error', 'No layer name ("nm")', layer.parse_type(), composition_name)
        if layer.id is None:
            self.set_error_or_warning('Error', f'No layer id ("ind") in {layer.name}', layer.parse_type(),
                                      composition_name)
        if layer.name is not None:
            self.eval_name(layer, layer.parse_type(), composition_name)

    def test_precomp_for_errors_and_warnings(self, precomp: Precomp):
        if precomp.name is None:
            self.set_error_or_warning('Warning', 'No precomp name ("nm")', 'pre composition', 'assets')
        if precomp.id is None:
            self.set_error_or_warning('Error', f'No precomp id ("id") in {precomp.name}', 'pre composition', 'assets')
        if precomp.name is not None:
            self.eval_name(precomp, 'precomp', 'assets')

    def test_image_for_errors_and_warnings(self, image: Image):
        if image.name is None:
            self.set_error_or_warning('Notice', 'No image name ("u")', 'image', 'assets')
        if image.id is None:
            self.set_error_or_warning('Error', f'No image id ("id") in {image.name}', 'image', 'assets')
        if image.name is not None:
            self.eval_name(image, 'image', 'assets')

    def analyze_lottie_main(self):
        lottie_main = Lottie_main(self.json_obj)
        if lottie_main.name is None:
            self.set_error_or_warning('Error', 'No lottie name ("nm")', 'lottie main', self.lottie_filename)
        if lottie_main.name is not None:
            self.eval_name(lottie_main, 'lottie main', self.lottie_filename)

    def analyze_shapes(self, shape_obj, parent, composition_name):
        shape_type = Lottie_parser.parse_shape_type(shape_obj)
        shape_id = Lottie_parser.parse_layer_id(shape_obj)
        shape_name = Lottie_parser.parse_layer_name(shape_obj)
        parent_id = parent.id
        if shape_name is None:
            shape_name = "None"
        if shape_id is None:
            shape_id = "None"

        node_item = Lottie_node(id=shape_id,
                                layer_type=shape_type,
                                name=shape_name,
                                composition_name=composition_name,
                                parent_id=parent_id,
                                parent=parent,
                                reference_id="shape_layer",
                                lottie_obj=shape_obj,
                                point_to_lottie_obj=self.point_to_lottie_obj)
        self.nodes.append(node_item)
        if shape_type == 'group' and 'it' in shape_obj:
            for shape_in_group in shape_obj['it']:
                self.analyze_shapes(shape_in_group, node_item, composition_name)

    def analyze_layers(self, analyze_shapes=True):
        for layer_id in self.layers:
            layer = self.layers[layer_id]
            composition_name = layer_id.split(':')[0]
            parent_id = self.parse_layer_parent(layer)
            node_item = Lottie_node(id=self.parse_layer_id(layer),
                                    layer_type=self.parse_layer_type(layer),
                                    name=self.parse_layer_name(layer),
                                    composition_name=composition_name,
                                    is_animated=self.is_layer_animated_or_non_static(layer),
                                    parent_id=parent_id,
                                    reference_id=self.parse_layer_reference(layer),
                                    lottie_obj=layer,
                                    point_to_lottie_obj=self.point_to_lottie_obj)
            self.nodes.append(node_item)
            self.test_layer_for_errors_and_warnings(Layer(layer), composition_name)
            if analyze_shapes:
                layer_type = self.parse_layer_type(self.layers[layer_id])
                if layer_type == 'shape' and 'shapes' in self.layers[layer_id]:
                    for shape in self.layers[layer_id]['shapes']:
                        self.analyze_shapes(shape, node_item, composition_name)

    def analyze_pre_compositions(self):
        pre_compositions = lsr.find_pre_comp(self.json_obj)
        if pre_compositions:
            for pre_composition_id in pre_compositions:
                pre_composition_node = Lottie_node(id=pre_composition_id,
                                                   name=self.parse_pre_comp_name(pre_compositions[pre_composition_id]),
                                                   layer_type="pre_composition",
                                                   composition_name='root',
                                                   lottie_obj=self.parse_pre_comp_layers(pre_compositions
                                                                                         [pre_composition_id]),
                                                   point_to_lottie_obj=self.point_to_lottie_obj)
                self.nodes.append(pre_composition_node)
                self.test_precomp_for_errors_and_warnings(Precomp(pre_compositions[pre_composition_id]))

    def analyze_assets(self):
        assets = lsr.find_assets(self.json_obj)
        if assets:
            for asset_id in assets:
                asset_node = Lottie_node(id=self.parse_asset_id(assets[asset_id]),
                                         name=self.parse_asset_name(assets[asset_id]),
                                         layer_type="image",
                                         lottie_obj=self.parse_pre_comp_layers(assets[asset_id]),
                                         point_to_lottie_obj=self.point_to_lottie_obj)
                self.nodes.append(asset_node)
                self.test_image_for_errors_and_warnings(Image(assets[asset_id]))

    def connect_nodes(self, flatten_pre_compositions=True):
        for node_item_1 in self.nodes[1:len(self.nodes)]:
            parent_id = node_item_1.parent_id
            reference_id = node_item_1.reference_id
            if parent_id is None:
                if node_item_1.composition_name == 'layers' or node_item_1.composition_name == 'root':
                    node_item_1.parent = self.nodes[0]
                    node_item_1.parent_id = self.nodes[0].id
                else:
                    for node_item_2 in self.nodes[1:len(self.nodes)]:
                        if node_item_1.composition_name == str(node_item_2.id):
                            node_item_1.parent = node_item_2
                            node_item_1.parent_id = node_item_2.id
            elif reference_id != "shape_layer":
                for node_item_2 in self.nodes[1:len(self.nodes)]:
                    if node_item_2.composition_name == node_item_1.composition_name and str(node_item_2.id) == str(
                            parent_id):
                        node_item_1.parent = node_item_2
                        node_item_1.parent_id = node_item_2.id
            if reference_id and reference_id != "shape_layer":
                for node_item_2 in self.nodes[1:len(self.nodes)]:
                    if node_item_2.id == reference_id:
                        if node_item_2.layer_type == 'image':
                            node_item_2.parent = node_item_1
                            node_item_2.parent_id = node_item_1.id
                        elif not flatten_pre_compositions and node_item_2.composition_name == 'root':
                            node_item_2.parent = node_item_1
                            node_item_2.parent_id = node_item_1.id

    def parse_warnings_and_errors(self):
        pass

    def analyze(self, flatten_pre_compositions=True, analyze_shapes=True, point_to_lottie_obj=False):
        self.lottie_file_size = stat(self.lottie_filename).st_size
        self.number_of_frames = self.parse_number_of_frames(self.json_obj)
        self.number_of_images = self.count_number_of_images()
        self.number_of_pre_comp = self.count_number_of_pre_compositions()
        self.number_of_main_layers = self.count_number_of_main_layers()
        self.point_to_lottie_obj = point_to_lottie_obj
        root_node = Lottie_node("root", "top node",
                                self.parse_lottie_name(self.json_obj),
                                lottie_obj=self.json_obj,
                                point_to_lottie_obj=self.point_to_lottie_obj)

        self.nodes.append(root_node)
        self.analyze_lottie_main()
        self.analyze_pre_compositions()
        self.analyze_assets()
        self.analyze_layers(analyze_shapes=analyze_shapes)
        self.connect_nodes(flatten_pre_compositions)
        self.parse_warnings_and_errors()

    def generate_analysis_report(self, to="console", layer_id=True, layer_type=True, is_animated=False, reference_id=False):
        lottie_file_name = self.lottie_filename
        lottie_file_size = str(self.lottie_file_size / 1000)
        lottie_number_of_layers = str(self.number_of_main_layers)
        if to == 'console':
            print(f'File name : {lottie_file_name}')
            print(f'file size : {lottie_file_size}KB')
            print(f'Number of main layers : {lottie_number_of_layers}')
            if self.number_of_pre_comp > 0:
                print(f'Number of pre compositions : {self.number_of_pre_comp}')
            if self.number_of_images > 0:
                print(f'Number of images : {self.number_of_images}')
        for pre, fill, node in RenderTree(la.nodes[0]):
            treestr = u"%s%s" % (pre, node.name)
            node_string = ""
            if layer_id:
                node_string += f'| id:{node.id} | '
            if layer_type:
                node_string += f'type:{node.layer_type} | '
            if is_animated:
                node_string += f'animated?{node.is_animated} | '
            if reference_id:
                node_string += f'ref:{node.reference_id} | '
            if to == 'console':
                print(treestr.ljust(8), node_string)
        if to == 'file':
            exporter = JsonExporter()
            file = open(self.lottie_filename.split('.')[0] + '_analysis.json', "w")
            analysis_str = exporter.export(la.nodes[0])
            analysis_str = analysis_str.replace("{", '{"File name":"' + lottie_file_name + '",'
                                                                                           '"File size":"' + lottie_file_size + 'KB",' +
                                                '"Number of main layers" :' + lottie_number_of_layers + ',' +
                                                '"Number of pre compositions" :' + str(self.number_of_pre_comp) + ',' +
                                                '"Number of images" :' + str(self.number_of_images) + ',', 1)
            file.write(analysis_str)
            file.close()

    def generate_errors_report(self, to="console"):
        if to == 'console':
            print(f'Number of errors: {self.errors_counter["errors"]}')
            print(f'Number of warnings: {self.errors_counter["warnings"]}')
            print(f'Number of notices: {self.errors_counter["notices"]}')
            for error in la.errors_and_warnings:
                print(la.errors_and_warnings[error])
        elif to == 'file':
            file = open(self.lottie_filename.split('.')[0] + '_errors.txt', "w")
            file.write(f'Number of errors: {self.errors_counter["errors"]}\n')
            file.write(f'Number of warnings: {self.errors_counter["warnings"]}\n')
            file.write(f'Number of notices: {self.errors_counter["notices"]}\n')
            for error in la.errors_and_warnings:
                file.write(la.errors_and_warnings[error] + '\n')
            file.close()


la = Lottie_analyzer('test-4.json')
la = Lottie_analyzer('Merry Christmas from Vidalgo doggie.json')
la = Lottie_analyzer('hanukkah.json')
la = Lottie_analyzer('new_year.json')
la = Lottie_analyzer('Birthday-Card.json')
la = Lottie_analyzer('coin.json')
la = Lottie_analyzer('D:\\Dropbox\\Vidalgo\\LottieFiles\\files1\\nyan-cat.json')
la = Lottie_analyzer('D:\\Dropbox\\Vidalgo\\LottieFiles\\files1\\Wacky-text-style1.json')
# la = Lottie_analyzer('D:\\Dropbox\\Vidalgo\\LottieFiles\\files1\\From Lottie Website\\42839-2021.json')
la = Lottie_analyzer(
    'D:\\Dropbox\\Vidalgo\\LottieFiles\\files1\\From Lottie Website\\33092-informatics-text-animation-with-icons-particles.json')
# la = Lottie_analyzer('D:\\Dropbox\\Vidalgo\\LottieFiles\\files1\\From Lottie Website\\33496-imron-textile-group.json')
# la = Lottie_analyzer('D:\\Dropbox\\Vidalgo\\LottieFiles\\files1\\From Lottie Website\\42803-loading.json')
la = Lottie_analyzer('4906-lady-guitar-player.json')
# la = Lottie_analyzer('38608-fashionable-girl-in-red-dress.json')
la = Lottie_analyzer('Merry Christmas from Vidalgo doggie.json')

la.analyze(flatten_pre_compositions=False, analyze_shapes=False, point_to_lottie_obj=False)
la.generate_analysis_report(to="file", layer_id=True, layer_type=True, is_animated=False, reference_id=True)
# la.visualize_to_text(to="file", layer_id=True, layer_type=True, is_animated=False, reference_id=True)

la.generate_errors_report(to="file")

'''udo = Node("Udo")
marc = Node("Marc", parent=udo)
lian = Node("Lian", parent=marc)
dan = Node("Dan", parent=udo)
jet = Node("Jet", parent=dan)
jan = Node("Jan", parent=dan)
joe = Node("Joe", parent=dan)

file = open("udo.png", 'w')
DotExporter(udo).to_picture("udo.png")
file.close()'''

pass
