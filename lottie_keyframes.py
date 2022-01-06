# This class holds a keyframe and member functions to crud its elements
class Text_keyframe:
    def __init__(self, keyframe_obj):
        if 't' in keyframe_obj:
            self.keyframe_obj = keyframe_obj
            self.transform_type = "text"
        else:
            raise Exception(f"Bad keyframe")

    def set_start_time(self, start_time):
        self.keyframe_obj['t'] = start_time

    def get_start_time(self):
        return self.keyframe_obj['t']

    def set_start_time(self, start_time):
        self.keyframe_obj['t'] = start_time

    def get_start_time(self):
        return self.keyframe_obj['t']



class Base_keyframe:
    def __init__(self, transform_type, keyframe_obj):
        if 't' in keyframe_obj and 'i' in keyframe_obj and 'o' in keyframe_obj:
            self.keyframe_obj = keyframe_obj
            self.transform_type = transform_type
        else:
            raise Exception(f"Bad keyframe")

    def set_start_time(self, start_time):
        self.keyframe_obj['t'] = start_time

    def get_start_time(self):
        return self.keyframe_obj['t']

    def set_in_value(self, in_value):
        self.keyframe_obj['i'] = in_value

    def get_in_value(self):
        return self.keyframe_obj['i']

    def set_out_value(self, out_value):
        self.keyframe_obj['o'] = out_value

    def get_out_value(self):
        return self.keyframe_obj['o']

    def set_jump_to_end(self, jump_to_end):
        if jump_to_end == 0 or jump_to_end == 1:
            self.keyframe_obj['h'] = jump_to_end
        else:
            raise Exception(f"Bad keyframe jump to end value : {jump_to_end}")

    def get_jump_to_end(self):
        if 'h' in self.keyframe_obj:
            return self.keyframe_obj['h']


class Position_keyframe(Base_keyframe):
    def __init__(self, transform_type, keyframe_obj):
        if 's' in keyframe_obj and 'e' in keyframe_obj and 'ti' in keyframe_obj and 'to' in keyframe_obj:
            Base_keyframe.__init__(transform_type, keyframe_obj)
        else:
            raise Exception(f"Bad position keyframe")

    def set_start_segment(self, start_segment):
        self.keyframe_obj['s'] = start_segment

    def get_start_segment(self):
        return self.keyframe_obj['s']

    def set_end_segment(self, end_segment):
        self.keyframe_obj['e'] = end_segment

    def get_end_segment(self):
        return self.keyframe_obj['e']

    def set_in_tangent(self, in_tangent):
        self.keyframe_obj['ti'] = in_tangent

    def get_in_tangent(self):
        return self.keyframe_obj['ti']

    def set_out_tangent(self, set_out_tangent):
        self.keyframe_obj['to'] = set_out_tangent

    def get_set_out_tangent(self):
        return self.keyframe_obj['to']


class Shape_keyframe(Base_keyframe):
    def __init__(self, transform_type, keyframe_obj):
        if 's' in keyframe_obj and 'e' in keyframe_obj:
            Base_keyframe.__init__(transform_type, keyframe_obj)
        else:
            raise Exception(f"Bad position keyframe")

    def set_start_segment(self, start_segment):
        self.keyframe_obj['s'] = start_segment

    def get_start_segment(self):
        return self.keyframe_obj['s']

    def set_end_segment(self, end_segment):
        self.keyframe_obj['e'] = end_segment

    def get_end_segment(self):
        return self.keyframe_obj['e']


# This class holds a list of keyframes for 1 transform (position / rotation / etc...) and member functions to CRUD key_frames
# This class recieves and
class keyframes_of_transform:
    def __init__(self, transform_type, keyframe_obj):
        if 'a' in keyframe_obj and keyframe_obj['a'] == 1:
            if transform_type == 'anchor' \
                    or transform_type == 'position' \
                    or transform_type == 'scale' \
                    or transform_type == 'orientation' \
                    or transform_type == 'rotation' \
                    or transform_type == 'skew' \
                    or transform_type == 'skew_axis' \
                    or transform_type == 'opacity':
                keyframe = Position_keyframe(transform_type, keyframe_obj)
            elif transform_type == 'rotation' or transform_type == 'skew' or transform_type == 'skew_axis'\
                    or transform_type == 'opacity':
                keyframe = Shape_keyframe(transform_type, keyframe_obj)
            else:
                self.transform_type = 'unknown'
            keyframe = Base_keyframe(transform_type, keyframe_obj)
