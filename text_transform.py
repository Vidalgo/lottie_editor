from static_transform import Static_transform
from static_transform import Lottie_transform_type
from transform import Transform


class Text_transform(Transform):
    def __init__(self, create_anchor=True, create_position=True, create_scale=True, create_rotation=True,
                 create_opacity=True, create_position_x=False, create_position_y=False, create_position_z=False,
                 create_skew=False, create_skew_axis=False, orientation=False, rotate_x=False, rotate_y=False,
                 stroke_width=False, stroke_color=False, fill_color=False, hue=False, saturation=False,
                 brightness=False, tracking=False):
        Transform.__init__(self, create_anchor, create_position, create_scale, create_rotation, create_opacity,
                           create_position_x, create_position_y, create_position_z, create_skew, create_skew_axis)
        self.orientation = orientation
        self.rotate_x = rotate_x
        self.rotate_y = rotate_y
        self.stroke_width = stroke_width
        self.stroke_color = stroke_color
        self.fill_color = fill_color
        self.hue = hue
        self.saturation = saturation
        self.brightness = brightness
        self.tracking = tracking
        self.analyze()

    def analyze(self):
        pass

    def load(self, transform: dict):
        self.transform = transform

    @property
    def orientation(self):
        if 'or' in self.transform:
            return self.transform['or']
        else:
            return None

    @orientation.setter
    def orientation(self, orientation):
        self.transform['or'] = None if orientation is None or orientation is False else \
            Static_transform(Lottie_transform_type.orientation, orientation).transform_object

    @property
    def rotate_x(self):
        if 'rotate_x' in self.transform:
            return self.transform['rotate_x']
        else:
            return None

    @rotate_x.setter
    def rotate_x(self, rotate_x):
        self.transform['rotate_x'] = None if rotate_x is None or rotate_x is False else \
            Static_transform(Lottie_transform_type.rotate_x, rotate_x).transform_object

    @property
    def rotate_y(self):
        if 'rotate_y' in self.transform:
            return self.transform['rotate_y']
        else:
            return None

    @rotate_y.setter
    def rotate_y(self, rotate_y):
        self.transform['rotate_y'] = None if rotate_y is None or rotate_y is False else \
            Static_transform(Lottie_transform_type.rotate_y, rotate_y).transform_object

    @property
    def stroke_width(self):
        if 'sw' in self.transform:
            return self.transform['sw']
        else:
            return None

    @stroke_width.setter
    def stroke_width(self, stroke_width):
        self.transform['sw'] = None if stroke_width is None or stroke_width is False else \
            Static_transform(Lottie_transform_type.stroke_width, stroke_width).transform_object

    @property
    def stroke_color(self):
        if 'sc' in self.transform:
            return self.transform['sc']
        else:
            return None

    @stroke_color.setter
    def stroke_color(self, stroke_color):
        self.transform['sc'] = None if stroke_color is None or stroke_color is False else \
            Static_transform(Lottie_transform_type.stroke_color, stroke_color).transform_object

    @property
    def fill_color(self):
        if 'fc' in self.transform:
            return self.transform['fc']
        else:
            return None

    @fill_color.setter
    def fill_color(self, fill_color):
        self.transform['fc'] = None if fill_color is None or fill_color is False else \
            Static_transform(Lottie_transform_type.fill_color, fill_color).transform_object

    @property
    def hue(self):
        if 'fh' in self.transform:
            return self.transform['fh']
        else:
            return None

    @hue.setter
    def hue(self, hue):
        self.transform['fh'] = None if hue is None or hue is False else \
            Static_transform(Lottie_transform_type.hue, hue).transform_object

    @property
    def saturation(self):
        if 'fs' in self.transform:
            return self.transform['fs']
        else:
            return None

    @saturation.setter
    def saturation(self, saturation):
        self.transform['fs'] = None if saturation is None or saturation is False else \
            Static_transform(Lottie_transform_type.saturation, saturation).transform_object

    @property
    def brightness(self):
        if 'fb' in self.transform:
            return self.transform['fb']
        else:
            return None

    @brightness.setter
    def brightness(self, brightness):
        self.transform['fb'] = None if brightness is None or brightness is False else \
            Static_transform(Lottie_transform_type.brightness, brightness).transform_object

    @property
    def tracking(self):
        if 't' in self.transform:
            return self.transform['t']
        else:
            return None

    @tracking.setter
    def tracking(self, tracking):
        self.transform['t'] = None if tracking is None or tracking is False else \
            Static_transform(Lottie_transform_type.tracking, tracking).transform_object
