import enum


class Lottie_transform_type(enum.Enum):
    anchor = 1
    position = 2
    scaling = 6
    rotation = 10
    opacity = 3
    position_x = 10
    position_y = 11
    position_z = 12
    Skew = 4
    Skew_axis = 5


class Static_transform:
    def __init__(self, transform_type: Lottie_transform_type, property_value=None, *args, **kwargs):
        self.transform_object = {}
        match transform_type.name:
            case 'anchor' | 'position':
                self.property_value = [0, 0, 0] if property_value is True else property_value
            case 'scaling':
                self.property_value = [100, 100, 100] if property_value is True else property_value
            case 'opacity':
                self.property_value = 100 if property_value is True else property_value
            case _:
                self.property_value = 0 if property_value is True else property_value
        self.property_index = transform_type.value
        self.animated = 0
        self.analyze()

    def analyze(self):
        if type(self.transform_object) is not dict:
            raise TypeError("Error: composition is not of type dictionary")
        if self.property_value is None:
            raise TypeError("Error: composition doesn't have a value")
        match Lottie_transform_type(self.property_index).name:
            case 'anchor' | 'position' | 'scaling':
                if type(self.property_value) is not list or len(self.property_value) < 2 or len(self.property_value) > 3:
                    raise TypeError("Error: not a list or incorrect dimension")
            case _:
                if type(self.property_value) is not float and type(self.property_value) is not int:
                    raise TypeError("Error: not a number")

    @property
    def property_value(self):
        if 'k' in self.transform_object:
            return (self.transform_object['k'] + [0])[0:3] if type(self.transform_object['k']) is list else \
                self.transform_object['k']
        else:
            return None

    @property_value.setter
    def property_value(self, property_value):
        self.transform_object['k'] = property_value

    @property
    def property_expression(self):
        if 'x' in self.transform_object:
            return self.transform_object['x']
        else:
            return None

    @property_expression.setter
    def property_expression(self, property_expression: str):
        self.transform_object['x'] = property_expression

    @property
    def property_index(self):
        if 'ix' in self.transform_object:
            return self.transform_object['ix']
        else:
            return None

    @property_index.setter
    def property_index(self, property_index: int):
        self.transform_object['ix'] = property_index

    @property
    def animated(self):
        if 'a' in self.transform_object:
            return self.transform_object['a']
        else:
            return None

    @animated.setter
    def animated(self, animated: int):
        self.transform_object['a'] = animated
