import engine.lottie_search_and_replace as lsr
import datetime
import random


class Lottie_parser:
    index = 0
    def __init__(self, lottie_filename_or_obj):
        if type(lottie_filename_or_obj) is str:
            self.lottie_filename = lottie_filename_or_obj
            self.json_obj = lsr.load_json(lottie_filename_or_obj)
        elif type(lottie_filename_or_obj) is dict:
            self.json_obj = lottie_filename_or_obj
        else:
            raise TypeError("Error: lottie input is not a filename nor a lottie object")
        self.assets = {}
        self.layers = {}
        random.seed(datetime.datetime.now().microsecond)

    def travel(self, data_object):
        def _expend_key(key_prefix, lottie_obj):
            lottie_obj_name = Lottie_parser.parse_layer_name(lottie_obj)
            lottie_obj_id = Lottie_parser.parse_layer_id(lottie_obj)
            lottie_obj_name = lottie_obj_name if lottie_obj_name is not None else "na_" + str(Lottie_parser.index)
            lottie_obj_id = str(lottie_obj_id) if lottie_obj_id is not None else "na_" + str(Lottie_parser.index)
            Lottie_parser.index += 1
            return key_prefix + '\\' + lottie_obj_name + ':' + str(lottie_obj_id)

        def _travel_shapes(shape_obj, inner_data_object, layer_key_prefix):
            layer_key_expended = _expend_key(layer_key_prefix, shape_obj)
            if shape_obj is not None and hasattr(data_object, 'parse_shape'):
                data_object.parse_shape(shape_obj, layer_key_expended)
            if shape_obj['ty'] == 'gr':
                if 'it' in shape_obj:
                    for inner_shape in shape_obj['it']:
                        _travel_shapes(inner_shape, inner_data_object, layer_key_expended)

        for layer_key in self.layers:
            layer_obj = self.layers[layer_key]
            if data_object is not None and hasattr(data_object, 'parse_layer'):
                data_object.parse_layer(layer_obj, layer_key)
            layer_type = self.parse_layer_type(layer_obj)
            if layer_type == 'shape' and 'shapes' in layer_obj:
                for shape in layer_obj['shapes']:
                    _travel_shapes(shape, data_object, layer_key)

    def parse_images(self):
        self.assets = lsr.find_assets(self.json_obj, "images")

    def parse_layers(self):
        self.layers = lsr.find_main_layers(self.json_obj)
        self.layers.update(lsr.find_pre_comp_layers(self.json_obj))

    def parse(self):
        self.parse_images()
        self.parse_layers()

    def store_lottie(self, file_name):
        lsr.store_json(file_name, self.json_obj)

    def get_layer(self, layer_id, composition="layers"):
        if not self.layers:
            return False
        key = str(composition) + ":" + str(layer_id)
        if key in self.layers:
            return self.layers[key]
        else:
            return {}

    def get_asset(self, layer_id, asset="image"):
        if not self.layers:
            return False
        key = str(asset) + ":" + str(layer_id)
        if key in self.assets:
            return self.assets[key]
        else:
            return {}

    def where_is_layer(self, layer_id):
        source = []
        if self.layers:
            for layer_key in self.layers.keys():
                if str(layer_id) == layer_key.split(':')[1]:
                    source.append(layer_key.split(':')[0])
        return source

    def get_layer_name(self, layer_id, composition="layers"):
        if not self.layers:
            return False
        key = str(composition) + ":" + str(layer_id)
        if key in self.layers and "nm" in self.layers[key]:
            return self.layers[key]["nm"]
        else:
            return False

    def get_pre_comp_name(self, pre_comp_id):
        if not self.layers:
            return False
        pre_comp = lsr.find_pre_comp(self.json_obj)
        if pre_comp_id in pre_comp and "nm" in pre_comp[pre_comp_id]:
            return pre_comp[pre_comp_id]["nm"]
        else:
            return False

    def get_layer_id(self, layer_name, composition="layers"):
        if not self.layers:
            return False

        for layer in self.layers:
            if layer.split(':')[0] == composition and "nm" in self.layers[layer] and self.layers[layer][
                "nm"] == layer_name:
                return layer.split(':')[1]

    def get_layer_parents_ids(self, layer_id, composition="layers"):
        if not self.layers:
            return False
        key = composition + ":" + str(layer_id)
        if key in self.layers:
            layer = self.layers[key]
        else:
            return False
        parents = []
        while 'parent' in layer:
            parent_id = layer['parent']
            key = composition + ":" + str(parent_id)
            if key in self.layers:
                layer = self.layers[key]
            else:
                return False
            parents.append(parent_id)
        return parents

    def get_layer_pre_composition_ref(self, layer_id, composition="layers"):
        if not self.layers:
            return False
        key = composition + ":" + str(layer_id)
        if key in self.layers:
            layer = self.layers[key]
        else:
            return False

        if "refId" in layer:
            return layer["refId"]

        return False

    def get_layer_transform(self, layer_id, composition="layers"):
        key = composition + ":" + str(layer_id)
        if key in self.layers and "ks" in self.layers[key]:
            return self.layers[key]["ks"]
        else:
            return False

    def add_layer(self, layer_obj, composition="layers", order="last", layer_id=""):
        if 'ind' in layer_obj:
            key = composition + ":" + str(layer_obj['ind'])
        else:
            return False
        new_lottie = lsr.add_layer(lottie_obj=self.json_obj, layer_obj=layer_obj, composition_id=composition,
                                   order=order, layer_id=layer_id)
        self.layers[key] = layer_obj
        return new_lottie

    def add_image(self, image_obj, order="last", layer_id=""):
        if 'id' in image_obj:
            key = "image:" + str(image_obj['id'])
        else:
            return False

        new_lottie = lsr.add_asset(lottie_obj=self.json_obj, asset_obj=image_obj, asset_key='images',
                                   order=order, layer_id=layer_id)
        self.assets[key] = image_obj
        return new_lottie

    def replace_layer(self, layer_id, new_layer_obj, composition='layers'):
        if "ind" in new_layer_obj:
            key = composition + ":" + str(layer_id)
            new_key = composition + ":" + str(new_layer_obj['ind'])
        else:
            return False
        new_lottie = lsr.replace_layer(lottie_obj=self.json_obj, layer_id=layer_id,
                                       new_layer_obj=new_layer_obj, composition_id=composition)
        if not new_lottie:
            return False
        del self.layers[key]
        self.layers[new_key] = new_layer_obj
        return new_lottie

    def replace_image(self, image_id, new_image_obj):
        if 'id' in new_image_obj:
            key = "image:" + str(image_id)
            new_key = "image:" + str(new_image_obj['id'])
        else:
            return False
        new_lottie = lsr.replace_asset(lottie_obj=self.json_obj, asset_id=image_id,
                                       new_asset_obj=new_image_obj, asset_key='images')
        if not new_lottie:
            return False
        del self.assets[key]
        self.assets[new_key] = new_image_obj
        return new_lottie

    def get_parent_id(self, layer_id, composition="layers"):
        layer = self.get_layer(layer_id, composition)
        if 'parent' in layer:
            return layer["parent"]
        else:
            return False

    def set_parent_id(self, parent_id, layer_id, composition="layers"):
        layer = self.get_layer(layer_id, composition, )
        layer["parent"] = parent_id

    def count_number_of_images(self):
        counter = 0
        for item in self.assets:
            if item.split(':')[0] == 'image':
                counter += 1
        return counter

    def count_number_of_pre_compositions(self):
        return len(lsr.find_pre_comp(self.json_obj))

    def count_number_of_main_layers(self):
        counter = 0
        for item in self.layers:
            if item.split(':')[0] == 'layers':
                counter += 1
        return counter

    @staticmethod
    def get_layer_obj_id(layer_obj):
        if "ind" in layer_obj:
            return layer_obj["ind"]
        elif "id" in layer_obj:
            return layer_obj["id"]
        else:
            return False

    @staticmethod
    def create_null_layer(name="NULL LAYER", id='', transform_obj=''):
        if type(id) is int:
            layer_id = id
        else:
            layer_id = int(random.random() * 100000)
        if transform_obj:
            transform_obj = transform_obj
        else:
            transform_obj = {"ks":
                                 {"a":
                                      {"a": 0,
                                       "k": [0, 0, 0],
                                       "ix": 1},
                                  "o":
                                      {"a": 0,
                                       "k": 0,
                                       "ix": 11},
                                  "p": {"a": 0,
                                        "k": [0, 0, 0],
                                        "ix": 2},
                                  "r": {"a": 0,
                                        "k": 0,
                                        "ix": 10},
                                  "s": {"a": 0,
                                        "k": [100, 100, 100],
                                        "ix": 6}}}

        return {"nm": name, "ty": 3, "ind": layer_id, "ks": transform_obj["ks"]}

    @staticmethod
    def parse_layer_id(layer):
        if 'ind' in layer:
            return layer['ind']
        elif 'cix' in layer:
            return layer['cix']
        elif 'ix' in layer:
            return layer['ix']
        else:
            return None

    @staticmethod
    def parse_layer_name(layer):
        if 'nm' in layer:
            return layer['nm']
        else:
            return None

    @staticmethod
    def parse_layer_parent(layer):
        if 'parent' in layer:
            return layer['parent']
        else:
            return None

    @staticmethod
    def parse_layer_reference(layer):
        if 'refId' in layer:
            return layer['refId']
        else:
            return None

    @staticmethod
    def parse_layer_type(layer):
        layer_type = layer["ty"]
        if layer_type == 0:
            return 'precomp'
        elif layer_type == 1:
            return 'solid'
        elif layer_type == 2:
            return 'image'
        elif layer_type == 3:
            return 'nullLayer'
        elif layer_type == 4:
            return 'shape'
        elif layer_type == 5:
            return 'text'
        elif layer_type == 6:
            return 'audio'
        elif layer_type == 7:
            return 'pholderVideo'
        elif layer_type == 8:
            return 'imageSeq'
        elif layer_type == 9:
            return 'video'
        elif layer_type == 10:
            return 'pholderStil'
        elif layer_type == 11:
            return 'guide'
        elif layer_type == 12:
            return 'adjustment'
        elif layer_type == 13:
            return 'camera'
        elif layer_type == 14:
            return 'light'
        elif layer_type == 15:
            return 'data'
        else:
            return 'unknown'

    @staticmethod
    def parse_shape_type(shape_layer):
        layer_type = shape_layer["ty"]
        if layer_type == 'fl':
            return 'fill'
        elif layer_type == 'gf':
            return 'gradient_fill'
        elif layer_type == 'gs':
            return 'gradient_stroke'
        elif layer_type == 'gr':
            return 'group'
        elif layer_type == 'mm':
            return 'merge'
        elif layer_type == 'rp':
            return 'repeater'
        elif layer_type == 'rd':
            return 'rounded_corners'
        elif layer_type == 'tm':
            return 'trim'
        elif layer_type == 'op':
            return 'offset_path'
        elif layer_type == 'pb':
            return 'pucker_bloat'
        elif layer_type == 'el':
            return 'ellipse'
        elif layer_type == 'sh':
            return 'path'
        elif layer_type == 'rc':
            return 'rectangle'
        elif layer_type == 'sr':
            return 'star'
        elif layer_type == 'st':
            return 'stroke'
        elif layer_type == 'tr':
            return 'transform'
        elif layer_type == 'tw':
            return 'twist'
        elif layer_type == 'zz':
            return 'zigzag'

    @staticmethod
    def parse_lottie_name(lottie_obj):
        if 'nm' in lottie_obj:
            return lottie_obj['nm']
        else:
            return None

    @staticmethod
    def parse_number_of_frames(lottie_obj):
        if 'fr' in lottie_obj:
            return lottie_obj['fr']
        else:
            return None

    @staticmethod
    def is_layer_animated_or_non_static(layer):
        animated = False
        transform = layer['ks']
        if 'a' in transform:
            if 'a' in transform['a'] and transform['a']['a']:
                animated = True
        if 'r' in transform:
            if 'a' in transform['r'] and transform['r']['a']:
                animated = True
        if 'p' in transform:
            if 'a' in transform['p'] and transform['p']['a']:
                animated = True
        if 's' in transform:
            if 'a' in transform['s'] and transform['s']['a']:
                animated = True
        return animated

    @staticmethod
    def parse_pre_comp_name(pre_composition_obj):
        if 'nm' in pre_composition_obj:
            return pre_composition_obj['nm']
        else:
            return None

    @staticmethod
    def parse_pre_comp_layers(pre_composition_obj):
        if 'layers' in pre_composition_obj:
            return pre_composition_obj['layers']
        else:
            return None

    @staticmethod
    def parse_asset_name(asset_obj):
        if 'id' in asset_obj:
            return asset_obj['id']

    @staticmethod
    def parse_asset_id(asset_obj):
        if 'id' in asset_obj:
            return asset_obj['id']

    @staticmethod
    def parse_layer_transform(layer):
        if 'ks' in layer:
            return layer['ks']


class Data_parser:
    obj_ref = dict()
    @staticmethod
    def _parse_color_from_shape(shape_obj, path):
        if shape_obj['ty'] == 'fl':
            if 'o' in shape_obj:
                opacity_key = '{0}\\opacity'.format(path)
                value = shape_obj['o']
                print('Shape type = {0}, Path = {1}, value = {2}'.format(Lottie_parser.parse_shape_type(shape_obj),
                                                                         opacity_key, value))
                Data_parser.obj_ref[opacity_key] = shape_obj
            if 'c' in shape_obj:
                color_key = '{0}\\color'.format(path)
                value = shape_obj['c']
                print('Shape type = {0}, Path = {1}, value = {2}'.format(Lottie_parser.parse_shape_type(shape_obj),
                                                                         color_key, value))
                Data_parser.obj_ref[color_key] = shape_obj

    @staticmethod
    def parse_shape(shape_obj, key):
        #print('Shape type = {0} Path = {1}'.format(Lottie_parser.parse_shape_type(shape_obj), key))
        Data_parser._parse_color_from_shape(shape_obj, key)

    @staticmethod
    def parse_layer(layer_obj, key):
        print('Layer type = {0} Path = {1}'.format(Lottie_parser.parse_layer_type(layer_obj), key))
        Data_parser.obj_ref[key] = layer_obj


if __name__ == '__main__':
    lp = Lottie_parser("D:\\lottie_files_path\\coin.json")
    #lp = Lottie_parser("D:\\lottie_files_path\\fairy.json")
    dp = Data_parser
    lp.parse()
    lp.travel(dp)
    dp.obj_ref['layers:0\\na_0:na_0\\na_2:na_2\\color']['c']['k'] = [5, 6, 7, 0]
    lp.store_lottie("D:\\lottie_files_path\\coin-1.json")
    pass


'''print(lp.get_layer(18419)["nm"])
print(lp.get_asset('image_9', 'image')["id"])
print(lp.get_layer(8, 'comp_0')["nm"])

print(lp.where_is_layer(1))
print(lp.where_is_layer(18419))
print(lp.where_is_layer('image_5'))

print(lp.get_layer_name(1))
print(lp.get_layer_name('image_6', 'images'))
print(lp.get_layer_name(1, 'comp_5'))

print(lp.get_layer_id('MARRY CHRISTMAS'))
print(lp.get_layer_id('image_6', 'images'))
print(lp.get_layer_id('5.png', 'comp_5'))

print(lp.get_layer_parents_ids(1))
print(lp.get_layer_parents_ids(1, 'comp_0'))

print(lp.get_layer_pre_composition_ref(3))
print(lp.get_layer_pre_composition_ref(1, 'comp_2'))

print(lp.get_layer_transform(3))
print(lp.get_layer_transform(1, 'comp_2'))

lp.create_null_layer()
print(lp.create_null_layer('MY_NULL'))
print(lp.create_null_layer('MY_NULL', 9999))
print(lp.create_null_layer('MY_NULL', 'abcd'))

image_layer = {"e": 1,"h": 1000,"w": 1000,"p":"data:image/png;base64,ABCD1234","u": "","id": "image_9999"}
null_layer = lp.create_null_layer()

lp.replace_image("image_5", image_layer)
lp.replace_layer(2, null_layer, "comp_2")
lp.replace_layer(18419, null_layer, "layers")

another_image_layer = {"e": 1,"h": 1000,"w": 1000,"p":"data:image/png;base64,ABCD1234","u": "","id": "image_11111"}
another_null_layer = lp.create_null_layer('MY_NULL', 9999)
print(lp.add_image(another_image_layer, order='before', layer_id="image_9999"))
print(lp.add_layer(another_null_layer, "comp_2", order='before', layer_id=1))
print(lp.add_layer(another_null_layer, "layers"))'''
