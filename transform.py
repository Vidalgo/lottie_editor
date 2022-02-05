import copy

from static_transform import Static_transform
from static_transform import Lottie_transform_type


class Transform:
    def __init__(self, create_anchor=True, create_position=True, create_scale=True, create_rotation=True,
                 create_opacity=True, create_position_x=False, create_position_y=False, create_position_z=False,
                 create_skew=False, create_skew_axis=False):
        self.transform = {}
        self.anchor = create_anchor
        self.position = create_position
        self.scaling = create_scale
        self.rotation = create_rotation
        self.opacity = create_opacity
        self.position_x = create_position_x
        self.position_y = create_position_y
        self.position_z = create_position_z
        self.skew = create_skew
        self.skew_axis = create_skew_axis
        self.analyze()

    def analyze(self):
        pass

    def load(self, transform: dict):
        self.transform = transform

    def copy(self, transform: dict):
        if type(transform) == type(self):
            self.transform = copy.deepcopy(transform.transform)
        else:
            self.transform = copy.deepcopy(transform)
        self.analyze()

    @property
    def anchor(self):
        if 'a' in self.transform:
            return self.transform['a']
        else:
            return None

    @anchor.setter
    def anchor(self, anchor):
        self.transform['a'] = None if anchor is None or anchor is False else \
            Static_transform(Lottie_transform_type.anchor, anchor).transform_object

    @property
    def position(self):
        if 'a' in self.transform:
            return self.transform['p']
        else:
            return None

    @position.setter
    def position(self, position):
        self.transform['p'] = None if position is None or position is False else \
            Static_transform(Lottie_transform_type.position, position).transform_object

    @property
    def scaling(self):
        if 's' in self.transform:
            return self.transform['s']
        else:
            return None

    @scaling.setter
    def scaling(self, scaling):
        self.transform['s'] = None if scaling is None or scaling is False else \
            Static_transform(Lottie_transform_type.scaling, scaling).transform_object

    @property
    def rotation(self):
        if 'r' in self.transform:
            return self.transform['r']
        else:
            return None

    @rotation.setter
    def rotation(self, rotation):
        self.transform['r'] = None if rotation is None or rotation is False else \
            Static_transform(Lottie_transform_type.rotation, rotation).transform_object

    @property
    def opacity(self):
        if 'o' in self.transform:
            return self.transform['o']
        else:
            return None

    @opacity.setter
    def opacity(self, opacity):
        self.transform['o'] = None if opacity is None or opacity is False else \
            Static_transform(Lottie_transform_type.opacity, opacity).transform_object

    @property
    def position_x(self):
        if 'px' in self.transform:
            return self.transform['px']
        else:
            return None

    @position_x.setter
    def position_x(self, position_x):
        self.transform['px'] = None if position_x is None or position_x is False else \
            Static_transform(Lottie_transform_type.position_x, position_x).transform_object

    @property
    def position_y(self):
        if 'py' in self.transform:
            return self.transform['py']
        else:
            return None

    @position_y.setter
    def position_y(self, position_y):
        self.transform['py'] = None if position_y is None or position_y is False else \
            Static_transform(Lottie_transform_type.position_y, position_y).transform_object

    @property
    def position_z(self):
        if 'pz' in self.transform:
            return self.transform['pz']
        else:
            return None

    @position_z.setter
    def position_z(self, position_z):
        self.transform['pz'] = None if position_z is None or position_z is False else \
            Static_transform(Lottie_transform_type.position_z, position_z).transform_object

    @property
    def skew(self):
        if 'sk' in self.transform:
            return self.transform['sk']
        else:
            return None

    @skew.setter
    def skew(self, skew):
        self.transform['sk'] = None if skew is None or skew is False else \
            Static_transform(Lottie_transform_type.skew, skew).transform_object

    @property
    def skew_axis(self):
        if 'sa' in self.transform:
            return self.transform['sa']
        else:
            return None

    @skew_axis.setter
    def skew_axis(self, skew_axis):
        self.transform['sa'] = None if skew_axis is None or skew_axis is False else \
            Static_transform(Lottie_transform_type.skew_axis, skew_axis).transform_object
