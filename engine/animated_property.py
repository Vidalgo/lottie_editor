import copy
from engine.keyframe import Keyframe


class Animated_property:
    def __init__(self, property_index: int = 0, animated: int = 0, keyframe=None):
        self._animated_property = {}
        self._keyframe = {}
        self.property_index = property_index
        self.animated = animated
        self.keyframe = keyframe

    def analyze(self):
        if type(self._animated_property) is not dict:
            raise TypeError("Error: animated property is not of type dictionary")
        if self.property_index is None:
            raise TypeError("Error: animated property doesn't have an index")
        if self.animated and type(self.keyframe) is not Keyframe:
            raise TypeError("Error: keyframe is not of type Keyframe")
        elif type(self.keyframe) is not float or type(self.keyframe) is not int or type(self.keyframe) is not \
                list[float] or type(self.keyframe) is not list[int]:
            raise TypeError("Error: keyframe is not of the correct property type")

    def load(self, animated_property: dict):
        self._animated_property = animated_property
        self._keyframe = Keyframe()
        self._keyframe.load(animated_property['k'])
        self.analyze()

    def copy(self, animated_property: dict):
        self._animated_property = copy.deepcopy(animated_property)
        self.analyze()

    @property
    def animated_property(self):
        return self._animated_property

    @animated_property.setter
    def animated_property(self, animated_property: dict):
        self._animated_property = animated_property
        self.analyze()

    @property
    def animated(self):
        if 'a' in self._animated_property:
            return self._animated_property['a']
        else:
            return 0

    @animated.setter
    def animated(self, property_value):
        self._animated_property['k'] = property_value

    @property
    def keyframe(self):
        return self._keyframe

    @keyframe.setter
    def keyframe(self, keyframe):
        self._keyframe = keyframe
        if self.animated:
            self._animated_property['k'] = keyframe.keyframe
        else:
            self._animated_property['k'] = keyframe

    @property
    def property_index(self):
        if 'ix' in self._animated_property:
            return self._animated_property['ix']
        else:
            return 0

    @property_index.setter
    def property_index(self, property_index: int):
        self._animated_property['ix'] = property_index

    @property
    def expression(self):
        if 'ix' in self._animated_property:
            return self._animated_property['x']
        else:
            return 0

    @expression.setter
    def expression(self, expression: str):
        self._animated_property['x'] = expression
