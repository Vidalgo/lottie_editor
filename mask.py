import copy
import enum
from animated_property import Animated_property


class Mask_mode(enum.Enum):
    No = 'n'
    Add = 'a'
    Subtract = 's'
    Intersect = 'i'
    Lighten = 'l'
    Darken = 'd'
    Difference = 'f'


class Mask:
    def __init__(self, mask_name: str = 'unknown', inverted: bool = False, shape=None, opacity=None,
                 mode=None, dilate=None):
        self._mask = {}
        self.mask_name = mask_name
        self.inverted = inverted
        self.shape = shape
        self.opacity = opacity
        self.mode = mode
        self.dilate = dilate

    def analyze(self):
        if type(self._mask) is not dict:
            raise TypeError("Error: mask is not of type dictionary")

    def load(self, mask: dict):
        self._mask = mask
        self.analyze()

    def copy(self, mask: dict):
        self._mask = copy.deepcopy(mask)
        self.analyze()

    @property
    def mask(self):
        return self._mask

    @mask.setter
    def mask(self, mask):
        self._mask = mask
        self.analyze()

    @property
    def name(self):
        if 'nm' in self._mask:
            return self._mask['nm']
        else:
            return None

    @name.setter
    def name(self, layer_name: str):
        self._mask['nm'] = layer_name

    @property
    def match_name(self):
        if 'mn' in self._mask:
            return self._mask['mn']
        else:
            return None

    @match_name.setter
    def match_name(self, match_name: str):
        self._mask['mn'] = match_name

    @property
    def inverted(self):
        if 'inv' in self._mask:
            return self._mask['inv']
        else:
            return None

    @inverted.setter
    def inverted(self, inverted: bool):
        self._mask['inv'] = inverted

    @property
    def opacity(self):
        if 'o' in self._mask:
            return self._mask['o']
        else:
            return None

    @opacity.setter
    def opacity(self, opacity: Animated_property):
        self._mask['o'] = opacity

    @property
    def mode(self):
        if 'mode' in self._mask:
            return self._mask['mode']
        else:
            return None

    @mode.setter
    def mode(self, mode: Mask_mode):
        self._mask['mode'] = mode.value

    @property
    def dilate(self):
        if 'x' in self._mask:
            return self._mask['x']
        else:
            return None

    @dilate.setter
    def dilate(self, dilate: Animated_property):
        self._mask['x'] = dilate
