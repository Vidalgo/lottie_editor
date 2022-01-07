# This class holds a keyframe and member functions to crud its elements
import copy


class Time_Keyframe:
    def __init__(self, key_frames_list):
        if not list(key_frames_list):
            raise Exception(f"Bad keyframe")

        self.key_frames_list = key_frames_list

    def get_keyframes(self, start_time=0, end_time=-1):
        key_frames_by_time = []
        if end_time == -1:
            end_time = self.key_frames_list[len(self.key_frames_list) - 1]['t'] + 1
        for index in range(len(self.key_frames_list)):
            keyframe_start_time = self.key_frames_list[index]['t']
            if index == len(self.key_frames_list) - 1:
                keyframe_end_time = end_time
            else:
                keyframe_end_time = self.key_frames_list[index + 1]['t']
            if keyframe_start_time <= start_time < keyframe_end_time or \
                    start_time <= keyframe_start_time < end_time:
                key_frames_by_time.append(self.key_frames_list[index])
        return key_frames_by_time

    def add_keyframes(self, new_key_frames_list):
        if not list(new_key_frames_list):
            raise Exception(f"Bad keyframe")
        for new_key_frame_obj in new_key_frames_list:
            new_keyframe_start_time = new_key_frame_obj['t']
            for index in range(len(self.key_frames_list)):
                keyframe_start_time = self.key_frames_list[index]['t']
                if new_keyframe_start_time < keyframe_start_time:
                    self.key_frames_list.insert(index, new_key_frame_obj)
                    break
                elif new_keyframe_start_time == keyframe_start_time:
                    self.key_frames_list.insert(index, new_key_frame_obj)
                    self.key_frames_list.pop(index + 1)
                    break
                elif index == len(self.key_frames_list) - 1:
                    self.key_frames_list.append(new_key_frame_obj)
        return self.key_frames_list

    def del_keyframes(self, start_time=0, end_time=-1):
        if end_time == -1:
            end_time = self.key_frames_list[len(self.key_frames_list) - 1]['t'] + 1
        index = 0
        while True:
            keyframe_start_time = self.key_frames_list[index]['t']
            if start_time <= keyframe_start_time < end_time:
                self.key_frames_list.pop(index)
            else:
                index += 1
            if index > len(self.key_frames_list) - 1:
                break
        return self.key_frames_list

    def scale_time(self, scale=1, start_time=0, end_time=-1):
        if end_time == -1:
            end_time = self.key_frames_list[len(self.key_frames_list) - 1]['t'] + 1
        new_keyframes = []
        for index in range(len(self.key_frames_list)):
            keyframe_start_time = self.key_frames_list[index]['t']
            if start_time < keyframe_start_time <= end_time:
                time_diff = keyframe_start_time - start_time
                if index != 0 and scale != 1 and not self.key_frames_list[index - 1]['t'] >= start_time:
                    new_keyframes.append(copy.deepcopy(self.key_frames_list[index - 1]))
                    new_keyframes[-1]['t'] = start_time
                self.key_frames_list[index]['t'] += time_diff * (scale - 1)
            elif keyframe_start_time > end_time:
                time_diff = end_time - start_time
                if scale != 1 and not self.key_frames_list[index - 1]['t'] >= start_time + time_diff * scale:
                    new_keyframes.append(copy.deepcopy(self.key_frames_list[index - 1]))
                    new_keyframes[-1]['t'] = start_time + time_diff * scale
                self.key_frames_list[index]['t'] += time_diff * (scale - 1)
        if new_keyframes:
            self.add_keyframes(new_keyframes)
        return self.key_frames_list

    @staticmethod
    def update_keyframe(start_time, keyframe_obj):
        keyframe_obj['t'] = start_time


class Text_keyframe(Time_Keyframe):
    def __init__(self, key_frames_list):
        Time_Keyframe.__init__(self, key_frames_list)
        self.transform_type = "text"

    @staticmethod
    def set_document(keyframe_obj, text_document):
        keyframe_obj['s'] = text_document

    @staticmethod
    def get_start_time(keyframe_obj):
        if 's' in keyframe_obj:
            return keyframe_obj['s']
        else:
            return None


class Base_keyframe(Time_Keyframe):
    def __init__(self, transform_type, key_frames_list):
        Time_Keyframe.__init__(self, key_frames_list)
        self.transform_type = transform_type

    @staticmethod
    def set_in_value(keyframe_obj, in_value):
        keyframe_obj['i'] = in_value

    @staticmethod
    def get_in_value(keyframe_obj):
        if 'i' in keyframe_obj:
            return keyframe_obj['i']
        else:
            return None

    @staticmethod
    def set_out_value(keyframe_obj, out_value):
        keyframe_obj['o'] = out_value

    @staticmethod
    def get_out_value(keyframe_obj):
        if 'o' in keyframe_obj:
            return keyframe_obj['o']
        else:
            return None

    @staticmethod
    def set_jump_to_end(keyframe_obj, jump_to_end):
        if jump_to_end == 0 or jump_to_end == 1:
            keyframe_obj['h'] = jump_to_end
        else:
            raise Exception(f"Bad keyframe jump to end value : {jump_to_end}")

    @staticmethod
    def get_jump_to_end(keyframe_obj):
        if 'h' in keyframe_obj:
            return keyframe_obj['h']


class Position_keyframe(Base_keyframe):
    def __init__(self, transform_type, key_frames_list):
        Base_keyframe.__init__(self, key_frames_list)
        self.transform_type = transform_type

    @staticmethod
    def set_start_segment(keyframe_obj, start_segment):
        keyframe_obj['s'] = start_segment

    @staticmethod
    def get_start_segment(keyframe_obj):
        if 's' in keyframe_obj:
            return keyframe_obj['s']
        else:
            return None

    @staticmethod
    def set_end_segment(keyframe_obj, end_segment):
        keyframe_obj['e'] = end_segment

    @staticmethod
    def get_end_segment(keyframe_obj):
        if 'e' in keyframe_obj:
            return keyframe_obj['e']
        else:
            return None

    @staticmethod
    def set_in_tangent(keyframe_obj, in_tangent):
        keyframe_obj['ti'] = in_tangent

    @staticmethod
    def get_in_tangent(keyframe_obj):
        return keyframe_obj['ti']

    @staticmethod
    def set_out_tangent(keyframe_obj, set_out_tangent):
        keyframe_obj['to'] = set_out_tangent

    @staticmethod
    def get_set_out_tangent(keyframe_obj):
        return keyframe_obj['to']


class Shape_keyframe(Base_keyframe):
    def __init__(self, transform_type, keyframe_obj):
        Base_keyframe.__init__(self, transform_type, keyframe_obj)

    @staticmethod
    def set_start_segment(keyframe_obj, start_segment):
        keyframe_obj['s'] = start_segment

    @staticmethod
    def get_start_segment(keyframe_obj):
        if 's' in keyframe_obj:
            return keyframe_obj['s']
        else:
            return None

    @staticmethod
    def set_end_segment(keyframe_obj, end_segment):
        keyframe_obj['e'] = end_segment

    @staticmethod
    def get_end_segment(keyframe_obj):
        if 's' in keyframe_obj:
            return keyframe_obj['e']
        else:
            return None


'''key_frames_list = [{'t': 18, 'o': 0}, {'t': 20, 'o': 1}, {'t': 35, 'o': 2}, {'t': 47, 'o': 3}, {'t': 50, 'o': 4}]

time_keyframe = Time_Keyframe(key_frames_list)
print(time_keyframe.get_keyframes())
print(time_keyframe.get_keyframes(0))
print(time_keyframe.get_keyframes(22))
print(time_keyframe.get_keyframes(28, 36))
print(time_keyframe.get_keyframes(0, 20))
print(time_keyframe.get_keyframes(13, 13))
print(time_keyframe.get_keyframes(13, 100))
print(time_keyframe.get_keyframes(35, 50))

print()
print(time_keyframe.get_keyframes())
new_key_frames_list = [{'t': 0, 'i': 0}, {'t': 15, 'i': 1}, {'t': 25, 'i': 2}, {'t': 35, 'i': 3}, {'t': 36, 'i': 4},
                       {'t': 46, 'i': 5},
                       {'t': 48, 'i': 6}, {'t': 54, 'i': 7}, {'t': 54, 'i': 8}, {'t': 60, 'i': 9}]
time_keyframe.add_keyframes(new_key_frames_list)
print(time_keyframe.get_keyframes())

print()
time_keyframe.del_keyframes(20, 50)
print(time_keyframe.get_keyframes())
print(time_keyframe.scale_time(2))
print(time_keyframe.scale_time(2, 15, 54))'''
