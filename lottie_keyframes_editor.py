from lottie_parser import Lottie_parser
import lottie_keyframes as kf


class Lottie_keyframe_editor(Lottie_parser):
    def __init__(self, lottie_filename):
        self.key_frames = {}
        self.keyframe_index = 0
        Lottie_parser.__init__(self, lottie_filename)

    @staticmethod
    def expend_key(keyframe_key_prefix, keyframe_key_name, keyframe_key_id):
        return keyframe_key_prefix + ',' + keyframe_key_name + ':' + str(keyframe_key_id)

    def add_to_keyframes(self, keyframe_key, keyframe):
        keyframe_key = self.expend_key(keyframe_key, 'root', self.keyframe_index)
        self.key_frames[keyframe_key] = keyframe
        self.keyframe_index += 1

    def set_keyframe_from_value(self, layer_key, layer_obj):
        if layer_obj['a'] == 1:
            keyframe_name = (layer_key.split(',')[-1]).split(':')[0]
            keyframe = kf.Shape_keyframe(keyframe_name, layer_obj['k'])
            self.add_to_keyframes(layer_key, keyframe)

    def set_keyframes_from_shape(self, layer_key, layer_obj):
        if 'cix' in layer_obj:
            index = layer_obj['cix']
        else:
            index = self.keyframe_index
        layer_key = self.expend_key(layer_key, 'shape', index)
        if layer_obj['ty'] == 'fl':
            shape_key = self.expend_key(layer_key, 'fill', index)
            if 'o' in layer_obj:
                shape_key = self.expend_key(shape_key, 'opacity', index)
                self.set_keyframe_from_value(shape_key, layer_obj['o'])
            if 'c' in layer_obj:
                shape_key = self.expend_key(shape_key, 'color_value', index)
                self.set_keyframe_from_value(shape_key, layer_obj['c'])
        elif layer_obj['ty'] == 'sh':
            shape_key = self.expend_key(layer_key, 'path', index)
            if 'ks' in layer_obj:
                shape_key = self.expend_key(shape_key, 'property', index)
                self.set_keyframe_from_value(shape_key, layer_obj['ks'])
        elif layer_obj['ty'] == 'gr':
            shape_key = self.expend_key(layer_key, 'group', index)
            if 'it' in layer_obj:
                for shape in layer_obj['it']:
                    self.set_keyframes_from_shape(shape_key, shape)

    def set_keyframes_from_mask_properties(self, layer_key, layer_obj):
        if 'masksProperties' in layer_obj:
            for index, mask_property in enumerate(layer_obj['masksProperties']):
                if 'o' in layer_obj['masksProperties']:
                    shape_key = self.expend_key(layer_key, 'masks_properties_opacity', index)
                    self.set_keyframe_from_value(shape_key, layer_obj['o'])
                if 'x' in layer_obj['masksProperties'] and layer_obj['masksProperties']['x']['a'] == 1:
                    shape_key = self.expend_key(layer_key, 'masks_properties_delate', index)
                    self.set_keyframe_from_value(shape_key, layer_obj['x'])

    def set_keyframes_from_layer_transform(self, layer_key, layer_obj):
        index = self.parse_layer_id(layer_obj)
        layer_key = self.expend_key(layer_key, 'transform', index)
        layer_obj = self.parse_layer_transform(layer_obj)
        if 'a' in layer_obj:
            shape_key = self.expend_key(layer_key, 'anchor', index)
            self.set_keyframe_from_value(shape_key, layer_obj['a'])
        if 'p' in layer_obj:
            shape_key = self.expend_key(layer_key, 'position', index)
            self.set_keyframe_from_value(shape_key, layer_obj['p'])
        if 's' in layer_obj:
            shape_key = self.expend_key(layer_key, 'scale', index)
            self.set_keyframe_from_value(shape_key, layer_obj['s'])
        if 'r' in layer_obj:
            shape_key = self.expend_key(layer_key, 'rotation', index)
            self.set_keyframe_from_value(shape_key, layer_obj['r'])
        if 'o' in layer_obj:
            shape_key = self.expend_key(layer_key, 'opacity', index)
            self.set_keyframe_from_value(shape_key, layer_obj['o'])
        if 'sk' in layer_obj:
            shape_key = self.expend_key(layer_key, 'skew', index)
            self.set_keyframe_from_value(shape_key, layer_obj['ak'])
        if 'sa' in layer_obj:
            shape_key = self.expend_key(layer_key, 'skew_axis', index)
            self.set_keyframe_from_value(shape_key, layer_obj['sa'])
        if 'or' in layer_obj:
            shape_key = self.expend_key(layer_key, 'orientation', index)
            self.set_keyframe_from_value(shape_key, layer_obj['or'])

    def get_keyframe(self, keyframe_sub_key):
        for keyframe_full_key in self.key_frames:
            if keyframe_full_key.find(keyframe_sub_key) != -1:
                return {keyframe_full_key: self.key_frames[keyframe_full_key]}

    def parse(self):
        Lottie_parser.parse(self)
        for layer_key in self.layers:
            self.set_keyframes_from_layer_transform(layer_key, self.layers[layer_key])
            self.set_keyframes_from_mask_properties(layer_key, self.layers[layer_key])
            layer_type = self.parse_layer_type(self.layers[layer_key])
            if layer_type == 'shape':
                for shape in self.layers[layer_key]['shapes']:
                    self.set_keyframes_from_shape(layer_key, shape)

    def get_layer_keyframes(self, layer_id, composition="layers"):
        layer_keyframes = {}
        keyframe_sub_key = composition+':'+str(layer_id)
        for keyframe_full_key in self.key_frames:
            if keyframe_full_key.find(keyframe_sub_key) != -1:
                layer_keyframes[keyframe_full_key] = self.key_frames[keyframe_full_key]
        return layer_keyframes

    def get_composition_keyframes(self, composition="layers"):
        composition_keyframes = {}
        keyframe_sub_key = composition
        for keyframe_full_key in self.key_frames:
            if keyframe_full_key.find(keyframe_sub_key) != -1:
                composition_keyframes[keyframe_full_key] = self.key_frames[keyframe_full_key]
        return composition_keyframes

lp = Lottie_keyframe_editor('Merry Christmas from Vidalgo doggie.json')
lp.parse()
for key_frame in lp.key_frames:
    print(key_frame)
print(lp.get_keyframe('comp_2'))
print(lp.get_keyframe('root:7'))
print(lp.get_layer_keyframes(2, 'comp_2'))
print(lp.get_composition_keyframes())
print(lp.get_composition_keyframes('comp_5'))
pass