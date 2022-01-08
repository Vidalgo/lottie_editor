from lottie_parser import Lottie_parser
import lottie_keyframes as kf


class Lottie_keyframe_editor(Lottie_parser):
    def __init__(self, lottie_filename):
        self.key_frames = {}
        self.keyframe_index = 0
        Lottie_parser.__init__(self, lottie_filename)

    def expend_key(self, keyframe_key_prefix, keyframe_key_name, layer_obj=None, find_name=False):
        keyframe_key_id = self.keyframe_index
        if layer_obj:
            if find_name:
                layer_name = Lottie_parser.parse_layer_name(layer_obj)
                if layer_name:
                    keyframe_key_name = layer_name            
            layer_id = Lottie_parser.parse_layer_id(layer_obj)
            if layer_id is not None:
                keyframe_key_id = layer_id

        return keyframe_key_prefix + ',' + keyframe_key_name + ':' + str(keyframe_key_id)

    def add_to_keyframes(self, keyframe_key, keyframe):
        keyframe_key = self.expend_key(keyframe_key, 'root')
        self.key_frames[keyframe_key] = keyframe
        self.keyframe_index += 1

    def set_keyframe_from_value(self, layer_key, layer_obj):
        if 'a' in layer_obj and layer_obj['a'] == 1:
            keyframe_name = (layer_key.split(',')[-1]).split(':')[0]
            keyframe = kf.Shape_keyframe(keyframe_name, layer_obj['k'])
            self.add_to_keyframes(layer_key, keyframe)

    def set_keyframe_from_text(self, text_key, layer_obj):
        keyframe = kf.Text_keyframe(layer_obj['k'])
        self.add_to_keyframes(text_key, keyframe)

    def set_keyframes_from_shape(self, layer_key, layer_obj):        
        #layer_key = self.expend_key(layer_key, 'shape', layer_obj, True)
        if layer_obj['ty'] == 'fl':
            shape_key = self.expend_key(layer_key, 'fill', layer_obj, True)
            if 'o' in layer_obj:
                shape_key = self.expend_key(shape_key, 'opacity', layer_obj, True)
                self.set_keyframe_from_value(shape_key, layer_obj['o'])
            if 'c' in layer_obj:                
                shape_key = self.expend_key(shape_key, 'color_value', layer_obj, True)
                self.set_keyframe_from_value(shape_key, layer_obj['c'])
        elif layer_obj['ty'] == 'gf':
            shape_key = self.expend_key(layer_key, 'gradient_fill', layer_obj, True)
            if 's' in layer_obj:
                shape_key = self.expend_key(shape_key, 'start_point', layer_obj, True)
                self.set_keyframe_from_value(shape_key, layer_obj['s'])
            if 'e' in layer_obj:
                shape_key = self.expend_key(shape_key, 'end_point', layer_obj, True)
                self.set_keyframe_from_value(shape_key, layer_obj['e'])
            if 'h' in layer_obj:
                shape_key = self.expend_key(shape_key, 'highlight_length', layer_obj, True)
                self.set_keyframe_from_value(shape_key, layer_obj['h'])
            if 'a' in layer_obj:
                shape_key = self.expend_key(shape_key, 'highlight_angle', layer_obj, True)
                self.set_keyframe_from_value(shape_key, layer_obj['a'])
            if 'g' in layer_obj and 'k' in layer_obj['g']:
                shape_key = self.expend_key(shape_key, 'colors', layer_obj, True)
                self.set_keyframe_from_value(shape_key, layer_obj['g']['k'])
            if 'o' in layer_obj:
                shape_key = self.expend_key(shape_key, 'opacity', layer_obj, True)
                self.set_keyframe_from_value(shape_key, layer_obj['o'])
        elif layer_obj['ty'] == 'gs':
            shape_key = self.expend_key(layer_key, 'gradient_stroke', layer_obj, True)
            if 'o' in layer_obj:
                shape_key = self.expend_key(shape_key, 'opacity', layer_obj, True)
                self.set_keyframe_from_value(shape_key, layer_obj['o'])
            if 'w' in layer_obj:
                shape_key = self.expend_key(shape_key, 'width', layer_obj, True)
                self.set_keyframe_from_value(shape_key, layer_obj['w'])
            if 'd' in layer_obj:
                shape_key = self.expend_key(shape_key, 'dash', layer_obj, True)
                for index_d, dash_obj in enumerate(layer_obj['d']):
                    if 'nm' in dash_obj:
                        dash_name = dash_obj['nm']
                    else:
                        dash_name = 'stroke_dash'
                    shape_key = self.expend_key(shape_key, 'dash', layer_obj, True)
                    self.set_keyframe_from_value(shape_key, dash_obj['v'])
            if 's' in layer_obj:
                shape_key = self.expend_key(shape_key, 'start_point', layer_obj, True)
                self.set_keyframe_from_value(shape_key, layer_obj['s'])
            if 'e' in layer_obj:
                shape_key = self.expend_key(shape_key, 'end_point', layer_obj, True)
                self.set_keyframe_from_value(shape_key, layer_obj['e'])
            if 'h' in layer_obj:
                shape_key = self.expend_key(shape_key, 'highlight_length', layer_obj, True)
                self.set_keyframe_from_value(shape_key, layer_obj['h'])
            if 'a' in layer_obj:
                shape_key = self.expend_key(shape_key, 'highlight_angle', layer_obj, True)
                self.set_keyframe_from_value(shape_key, layer_obj['a'])
            if 'g' in layer_obj and 'k' in layer_obj['g']:
                shape_key = self.expend_key(shape_key, 'colors', layer_obj, True)
                self.set_keyframe_from_value(shape_key, layer_obj['g']['k'])
        elif layer_obj['ty'] == 'rp':
            shape_key = self.expend_key(layer_key, 'repeater', layer_obj, True)
            if 'c' in layer_obj:
                shape_key = self.expend_key(shape_key, 'number_of_copies', layer_obj, True)
                self.set_keyframe_from_value(shape_key, layer_obj['c'])
            if 'o' in layer_obj:
                shape_key = self.expend_key(shape_key, 'offset_of_copies', layer_obj, True)
                self.set_keyframe_from_value(shape_key, layer_obj['o'])
            if 'tr' in layer_obj:
                self.set_keyframes_from_layer_transform(shape_key, layer_obj['tr'])
        elif layer_obj['ty'] == 'rd':
            shape_key = self.expend_key(layer_key, 'rounded_corners', layer_obj, True)
            if 'r' in layer_obj:
                shape_key = self.expend_key(shape_key, 'radius', layer_obj, True)
                self.set_keyframe_from_value(shape_key, layer_obj['r'])
        elif layer_obj['ty'] == 'tm':
            shape_key = self.expend_key(layer_key, 'trim', layer_obj, True)
            if 's' in layer_obj:
                shape_key = self.expend_key(shape_key, 'start_segment', layer_obj, True)
                self.set_keyframe_from_value(shape_key, layer_obj['s'])
            if 'e' in layer_obj:
                shape_key = self.expend_key(shape_key, 'end_segment', layer_obj, True)
                self.set_keyframe_from_value(shape_key, layer_obj['e'])
            if 'o' in layer_obj:
                shape_key = self.expend_key(shape_key, 'offset_angle', layer_obj, True)
                self.set_keyframe_from_value(shape_key, layer_obj['o'])
        elif layer_obj['ty'] == 'pb':
            shape_key = self.expend_key(layer_key, 'pucker_bloat', layer_obj, True)
            if 'a' in layer_obj:
                shape_key = self.expend_key(shape_key, 'amount', layer_obj, True)
                self.set_keyframe_from_value(shape_key, layer_obj['a'])
        elif layer_obj['ty'] == 'el':
            shape_key = self.expend_key(layer_key, 'ellipse', layer_obj, True)
            if 'p' in layer_obj:
                shape_key = self.expend_key(shape_key, 'position', layer_obj, True)
                self.set_keyframe_from_value(shape_key, layer_obj['p'])
            if 's' in layer_obj:
                shape_key = self.expend_key(shape_key, 'size', layer_obj, True)
                self.set_keyframe_from_value(shape_key, layer_obj['s'])
        elif layer_obj['ty'] == 'sh':
            shape_key = self.expend_key(layer_key, 'path', layer_obj, True)
            if 'ks' in layer_obj:
                shape_key = self.expend_key(shape_key, 'property', layer_obj['ks'], True)
                self.set_keyframe_from_value(shape_key, layer_obj['ks'])
        elif layer_obj['ty'] == 'rc':
            shape_key = self.expend_key(layer_key, 'rectangle', layer_obj, True)
            if 'p' in layer_obj:
                shape_key = self.expend_key(shape_key, 'position', layer_obj, True)
                self.set_keyframe_from_value(shape_key, layer_obj['p'])
            if 's' in layer_obj:
                shape_key = self.expend_key(shape_key, 'size', layer_obj, True)
                self.set_keyframe_from_value(shape_key, layer_obj['s'])
            if 'r' in layer_obj:
                shape_key = self.expend_key(shape_key, 'rounded_corners', layer_obj, True)
                self.set_keyframe_from_value(shape_key, layer_obj['r'])
        elif layer_obj['ty'] == 'sr':
            shape_key = self.expend_key(layer_key, 'star', layer_obj, True)
            if 'p' in layer_obj:
                shape_key = self.expend_key(shape_key, 'position', layer_obj, True)
                self.set_keyframe_from_value(shape_key, layer_obj['p'])
            if 'ir' in layer_obj:
                shape_key = self.expend_key(shape_key, 'inner_radius', layer_obj, True)
                self.set_keyframe_from_value(shape_key, layer_obj['ir'])
            if 'is' in layer_obj:
                shape_key = self.expend_key(shape_key, 'inner_roundness', layer_obj, True)
                self.set_keyframe_from_value(shape_key, layer_obj['is'])
            if 'or' in layer_obj:
                shape_key = self.expend_key(shape_key, 'outer_radius', layer_obj, True)
                self.set_keyframe_from_value(shape_key, layer_obj['or'])
            if 'os' in layer_obj:
                shape_key = self.expend_key(shape_key, 'outer_roundness', layer_obj, True)
                self.set_keyframe_from_value(shape_key, layer_obj['os'])
            if 'r' in layer_obj:
                shape_key = self.expend_key(shape_key, 'rounded_corners', layer_obj, True)
                self.set_keyframe_from_value(shape_key, layer_obj['r'])
            if 'pt' in layer_obj:
                shape_key = self.expend_key(shape_key, 'points_number', layer_obj, True)
                self.set_keyframe_from_value(shape_key, layer_obj['pt'])
        elif layer_obj['ty'] == 'st':
            shape_key = self.expend_key(layer_key, 'stroke', layer_obj, True)
            if 'o' in layer_obj:
                shape_key = self.expend_key(shape_key, 'opacity', layer_obj, True)
                self.set_keyframe_from_value(shape_key, layer_obj['o'])
            if 'w' in layer_obj:
                shape_key = self.expend_key(shape_key, 'width', layer_obj, True)
                self.set_keyframe_from_value(shape_key, layer_obj['w'])
            if 'd' in layer_obj:
                shape_key = self.expend_key(shape_key, 'dashes', layer_obj, True)
                for index_d, dash in enumerate(layer_obj['d']):
                    if 'v' in dash:
                        shape_key = self.expend_key(shape_key, 'stroke_dash', layer_obj, True)
                        self.set_keyframes_from_shape(shape_key, dash['v'])
            if 'c' in layer_obj:
                shape_key = self.expend_key(shape_key, 'color', layer_obj, True)
                self.set_keyframe_from_value(shape_key, layer_obj['c'])
        elif layer_obj['ty'] == 'tr':
            self.set_keyframes_from_layer_transform(layer_key, layer_obj)
        elif layer_obj['ty'] == 'tw':
            shape_key = self.expend_key(layer_key, 'twist', layer_obj, True)
            if 'a' in layer_obj:
                shape_key = self.expend_key(shape_key, 'angle', layer_obj, True)
                self.set_keyframe_from_value(shape_key, layer_obj['a'])
            if 'c' in layer_obj:
                shape_key = self.expend_key(shape_key, 'center', layer_obj, True)
                self.set_keyframe_from_value(shape_key, layer_obj['c'])
        elif layer_obj['ty'] == 'zz':
            shape_key = self.expend_key(layer_key, 'zigzag', layer_obj, True)
            if 'r' in layer_obj:
                shape_key = self.expend_key(shape_key, 'radius', layer_obj, True)
                self.set_keyframe_from_value(shape_key, layer_obj['r'])
            if 's' in layer_obj:
                shape_key = self.expend_key(shape_key, 'peaks_troughs_distance', layer_obj, True)
                self.set_keyframe_from_value(shape_key, layer_obj['s'])
            if 'pt' in layer_obj:
                shape_key = self.expend_key(shape_key, 'ridges_number', layer_obj, True)
                self.set_keyframe_from_value(shape_key, layer_obj['pt'])
        elif layer_obj['ty'] == 'gr':
            shape_key = self.expend_key(layer_key, 'group', layer_obj, True)
            if 'it' in layer_obj:
                for shape in layer_obj['it']:
                    self.set_keyframes_from_shape(shape_key, shape)

    def set_keyframes_from_text_animator_data(self, layer_key, layer_obj):
        if 'a' in layer_obj:
            text_key = self.expend_key(layer_key, 'animator_data', layer_obj, True)
            for text_animator_obj in layer_obj['a']:
                self.set_keyframes_from_layer_transform(text_key, text_animator_obj)
        if 'd' in layer_obj:
            text_key = self.expend_key(layer_key, 'data', layer_obj['d'], True)
            self.set_keyframe_from_text(text_key, layer_obj['d'])
        if 'm' in layer_obj:
            text_key = self.expend_key(layer_key, 'more_options', layer_obj, True)
            if 'a' in layer_obj['m']:
                text_key = self.expend_key(text_key, 'alignment', layer_obj['m']['a'], True)
                self.set_keyframe_from_value(text_key, layer_obj['m']['a'])
        if 'p' in layer_obj:
            text_key = self.expend_key(layer_key, 'masked_path', layer_obj, True)
            if 'f' in layer_obj['p']:
                text_key = self.expend_key(text_key, 'first', layer_obj['p']['f'], True)
                self.set_keyframe_from_value(text_key, layer_obj['p']['f'])
            if 'l' in layer_obj['p']:
                text_key = self.expend_key(text_key, 'last', layer_obj['p']['l'], True)
                self.set_keyframe_from_value(text_key, layer_obj['p']['l'])

    def set_keyframes_from_mask_properties(self, layer_key, layer_obj):
        if 'masksProperties' in layer_obj:
            for mask_property_obj in layer_obj['masksProperties']:
                if 'o' in mask_property_obj:
                    shape_key = self.expend_key(layer_key, 'masks_properties_opacity', mask_property_obj['o'], True)
                    self.set_keyframe_from_value(shape_key, mask_property_obj['o'])
                if 'x' in mask_property_obj:
                    shape_key = self.expend_key(layer_key, 'masks_properties_delate', mask_property_obj['x'], True)
                    self.set_keyframe_from_value(shape_key, mask_property_obj['x'])

    def set_keyframes_from_layer_transform(self, layer_key, layer_obj):
        #layer_key = self.expend_key(layer_key, 'transform', layer_obj, True)
        if 'a' in layer_obj:
            shape_key = self.expend_key(layer_key, 'anchor', layer_obj['a'], True)
            self.set_keyframe_from_value(shape_key, layer_obj['a'])
        if 'p' in layer_obj:
            shape_key = self.expend_key(layer_key, 'position', layer_obj['p'], True)
            self.set_keyframe_from_value(shape_key, layer_obj['p'])
        if 's' in layer_obj:
            shape_key = self.expend_key(layer_key, 'scale', layer_obj['s'], True)
            self.set_keyframe_from_value(shape_key, layer_obj['s'])
        if 'r' in layer_obj:
            shape_key = self.expend_key(layer_key, 'rotation', layer_obj['r'], True)
            self.set_keyframe_from_value(shape_key, layer_obj['r'])
        if 'rx' in layer_obj:
            shape_key = self.expend_key(layer_key, 'rotate_x', layer_obj['rx'], True)
            self.set_keyframe_from_value(shape_key, layer_obj['rx'])
        if 'ry' in layer_obj:
            shape_key = self.expend_key(layer_key, 'rotate_y', layer_obj['ry'], True)
            self.set_keyframe_from_value(shape_key, layer_obj['ry'])
        if 'o' in layer_obj:
            shape_key = self.expend_key(layer_key, 'opacity', layer_obj['o'], True)
            self.set_keyframe_from_value(shape_key, layer_obj['o'])
        if 'sk' in layer_obj:
            shape_key = self.expend_key(layer_key, 'skew', layer_obj['sk'], True)
            self.set_keyframe_from_value(shape_key, layer_obj['sk'])
        if 'sa' in layer_obj:
            shape_key = self.expend_key(layer_key, 'skew_axis', layer_obj['sa'], True)
            self.set_keyframe_from_value(shape_key, layer_obj['sa'])
        if 'or' in layer_obj:
            shape_key = self.expend_key(layer_key, 'orientation', layer_obj['or'], True)
            self.set_keyframe_from_value(shape_key, layer_obj['or'])
        if 'so' in layer_obj:
            shape_key = self.expend_key(layer_key, 'start_opacity', layer_obj['so'], True)
            self.set_keyframe_from_value(shape_key, layer_obj['so'])
        if 'eo' in layer_obj:
            shape_key = self.expend_key(layer_key, 'end_opacity', layer_obj['eo'], True)
            self.set_keyframe_from_value(shape_key, layer_obj['eo'])
        if 'sw' in layer_obj:
            shape_key = self.expend_key(layer_key, 'end_opacity', layer_obj['sw'], True)
            self.set_keyframe_from_value(shape_key, layer_obj['sw'])
        if 'sc' in layer_obj:
            shape_key = self.expend_key(layer_key, 'stroke_color', layer_obj['sc'], True)
            self.set_keyframe_from_value(shape_key, layer_obj['sc'])
        if 'fc' in layer_obj:
            shape_key = self.expend_key(layer_key, 'fill_color', layer_obj['fc'], True)
            self.set_keyframe_from_value(shape_key, layer_obj['fc'])
        if 'fh' in layer_obj:
            shape_key = self.expend_key(layer_key, 'hue', layer_obj['fh'], True)
            self.set_keyframe_from_value(shape_key, layer_obj['fh'])
        if 'fs' in layer_obj:
            shape_key = self.expend_key(layer_key, 'saturation', layer_obj['fs'], True)
            self.set_keyframe_from_value(shape_key, layer_obj['fs'])
        if 'fb' in layer_obj:
            shape_key = self.expend_key(layer_key, 'brightness', layer_obj['fs'], True)
            self.set_keyframe_from_value(shape_key, layer_obj['fs'])
        if 't' in layer_obj:
            shape_key = self.expend_key(layer_key, 'tracking', layer_obj['t'], True)
            self.set_keyframe_from_value(shape_key, layer_obj['t'])

    def get_keyframe(self, keyframe_sub_key):
        for keyframe_full_key in self.key_frames:
            if keyframe_full_key.find(keyframe_sub_key) != -1:
                return {keyframe_full_key: self.key_frames[keyframe_full_key]}

    def parse(self):
        Lottie_parser.parse(self)
        for layer_key in self.layers:
            layer_transform_obj = self.parse_layer_transform(self.layers[layer_key])
            layer_obj = self.layers[layer_key]
            pre_comp_name = self.get_pre_comp_name(layer_key.split(':')[0])
            if pre_comp_name:
                layer_key = pre_comp_name + ':' + layer_key.split(':')[0]
            layer_key = self.expend_key(layer_key, '', layer_obj, True)
            self.set_keyframes_from_layer_transform(layer_key, layer_transform_obj)
            self.set_keyframes_from_mask_properties(layer_key, layer_obj)
            layer_type = self.parse_layer_type(layer_obj)
            if layer_type == 'shape' and 'shapes' in layer_obj:
                for shape in layer_obj['shapes']:
                    self.set_keyframes_from_shape(layer_key, shape)
            elif layer_type == 'text' and 't' in layer_obj:
                self.set_keyframes_from_text_animator_data(layer_key, layer_obj['t'])
            elif layer_type == 'precomp' and 'tm' in layer_obj:
                precomp_key = self.expend_key(layer_key, 'time_remapping', layer_obj['tm'], True)
                self.set_keyframe_from_value(precomp_key, layer_obj['tm'])

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
lp = Lottie_keyframe_editor('Birthday-Card.json')

lp.parse()
for key_frame in lp.key_frames:
    print(key_frame)
for key_frame in lp.key_frames:
    print(lp.key_frames[key_frame].transform_type)
print(lp.get_keyframe('comp_2'))
print(lp.get_keyframe('root:7'))
print(lp.get_layer_keyframes(2, 'comp_2'))
print(lp.get_composition_keyframes())
print(lp.get_composition_keyframes('comp_5'))
pass