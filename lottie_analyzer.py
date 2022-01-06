import sys

from anytree import NodeMixin, Node, RenderTree
from anytree.exporter import DotExporter
from anytree.exporter import JsonExporter

import lottie_search_and_replace as lsr
from lottie_parser import Lottie_parser
from os import stat


class Lottie_node(NodeMixin):
    def __init__(self, id, layer_type, name=None, composition_name=None, is_animated=False, parent_id=None,
                 lottie_obj=None, parent=None, reference_id=None, children=None):
        self.id = id
        self.layer_type = layer_type
        self.name = name
        self.composition_name = composition_name
        self.is_animated = is_animated
        self.parent_id = parent_id
        self.lottie_obj = lottie_obj
        self.parent = parent
        self.reference_id = reference_id
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
        except:
            raise Exception(f"Error:could not open JSON file {lottie_filename}")

    def analyze_layers(self, pre_comp=True, shapes=True):
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
                                    lottie_obj=layer)
            if pre_comp and composition_name != "layers":
                self.nodes.append(node_item)
            else:
                self.nodes.append(node_item)

    def analyze_pre_compositions(self):
        pre_compositions = lsr.find_pre_comp(self.json_obj)
        if pre_compositions:
            for pre_composition_id in pre_compositions:
                pre_composition_node = Lottie_node(id=pre_composition_id,
                                                   name=self.parse_pre_comp_name(pre_compositions[pre_composition_id]),
                                                   layer_type="pre_composition",
                                                   composition_name='root',
                                                   lottie_obj=self.parse_pre_comp_layers(pre_compositions
                                                                                         [pre_composition_id]))
                self.nodes.append(pre_composition_node)

    def analyze_assets(self):
        assets = lsr.find_assets(self.json_obj)
        if assets:
            for asset_id in assets:
                asset_node = Lottie_node(id=self.asset_id(assets[asset_id]),
                                         name=self.asset_name(assets[asset_id]),
                                         layer_type="image",
                                         lottie_obj=self.parse_pre_comp_layers(assets[asset_id]))
                self.nodes.append(asset_node)

    def connect_nodes(self, flatten_pre_compositions=True):
        for node_item_1 in self.nodes[1:len(self.nodes)]:
            parent_id = node_item_1.parent_id
            reference_id = node_item_1.reference_id
            if parent_id is None:
                if node_item_1.composition_name == 'layers' or node_item_1.composition_name == 'root':
                    node_item_1.parent = self.nodes[0]
                else:
                    for node_item_2 in self.nodes[1:len(self.nodes)]:
                        if node_item_1.composition_name == str(node_item_2.id):
                                node_item_1.parent = node_item_2
            else:
                for node_item_2 in self.nodes[1:len(self.nodes)]:
                    if node_item_2.id == parent_id:
                        node_item_1.parent = node_item_2
            if reference_id:
                for node_item_2 in self.nodes[1:len(self.nodes)]:
                    if node_item_2.id == reference_id:
                        if node_item_2.layer_type == 'image' or not flatten_pre_compositions:
                            node_item_2.parent = node_item_1

    def analyze(self, pre_comp=True, flatten_pre_compositions=True, shapes=True):
        self.lottie_file_size = stat(self.lottie_filename).st_size
        self.number_of_frames = self.parse_number_of_frames(self.json_obj)
        self.number_of_images = self.count_number_of_images()
        self.number_of_pre_comp = self.count_number_of_pre_compositions()
        self.number_of_main_layers = self.count_number_of_main_layers()

        root_node = Lottie_node("root", "top node",
                                self.parse_lottie_name(self.json_obj),
                                lottie_obj=self.json_obj)

        self.nodes.append(root_node)
        self.analyze_pre_compositions()
        self.analyze_assets()
        self.analyze_layers(pre_comp=pre_comp, shapes=shapes)
        self.connect_nodes(flatten_pre_compositions)

    def visualize_to_text(self, to="console", layer_id=True, layer_type=True, is_animated=False, reference_id=False):
        print(f'File name : {self.lottie_filename}')
        print(f'File size : {self.lottie_file_size / 1000} KB')
        print(f'Number of main layers : {self.number_of_main_layers}')
        tree_file = open(self.lottie_filename.split('.')[0]+'.txt', 'w')
        if self.number_of_pre_comp > 0 :
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
            elif to == 'file':
                #sys.stdout = tree_file
                print(treestr.ljust(8), node_string)
        tree_file.close()

    def visualize_to_image(self, what="all", filename=""):
        if not filename:
            filename = self.lottie_filename.split('.')[0]+'.png'
            filename = "test.png"
            file = open(filename, 'w')
            DotExporter(la.nodes[0]).to_picture(filename)
            file.close()


la = Lottie_analyzer('test-4.json')
la = Lottie_analyzer('Merry Christmas from Vidalgo doggie.json')
la = Lottie_analyzer('hanukkah.json')
la = Lottie_analyzer('new_year.json')

la.analyze(flatten_pre_compositions=True)
la.visualize_to_text(to="file", layer_id=False, layer_type=True, is_animated=True, reference_id=False)
#la.visualize_to_image()

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
