import copy
from helpers import generate_random_id, VIDALGO_ID


class Char:
    def __init__(self, character: str = None, font_family: str = None, font_size: float = 0,
                 font_style: str = "normal", width: float = 0, data=None):
        self._char = {}
        self._data = {}
        self.character = character
        self.font_family = font_family
        self.font_size = font_size
        self.font_style = font_style
        self.width = width
        self.data = data
        generate_random_id(self._char)

    def analyze(self):
        if type(self._char) is not dict:
            raise TypeError("Error: layer is not of type dictionary")
        if self.data is None:
            raise TypeError("Error: char doesn't have data")
        if self.character is None:
            raise TypeError("Error: char doesn't have an character name")
        if self.font_family is None:
            raise TypeError("Error: char doesn't have a font family")
        if self.font_size is None:
            raise TypeError("Error: char doesn't have a font size")
        if self.font_style is None:
            raise TypeError("Error: char doesn't have a font style")
        if self.width is None:
            raise TypeError("Error: char doesn't have a font width")
        if self.vidalgo_id is None:
            raise TypeError("Error: char doesn't have a vidalgo id")

    def load(self, char: dict):
        self._char = char
        # self.data.load(char['data'])
        generate_random_id(self._char)
        self.analyze()

    def copy(self, font: dict):
        self.char = copy.deepcopy(font)
        self.analyze()

    @property
    def vidalgo_id(self):
        if VIDALGO_ID in self._char:
            return self._char[VIDALGO_ID]
        else:
            return None

    @vidalgo_id.setter
    def vidalgo_id(self, vidalgo_id: str):
        self._char[VIDALGO_ID] = vidalgo_id

    @property
    def char(self):
        return self._char

    @char.setter
    def char(self, char):
        self._char = char
        self.analyze()

    @property
    def character(self):
        if 'ch' in self._char:
            return self._char['ch']
        else:
            return None

    @character.setter
    def character(self, ascent: character):
        self._char['ch'] = ascent

    @property
    def font_family(self):
        if 'fFamily' in self._char:
            return self._char['fFamily']
        else:
            return None

    @font_family.setter
    def font_family(self, font_family: str):
        self._char['fFamily'] = font_family

    @property
    def font_size(self):
        if 'size' in self._char:
            return self._char['size']
        else:
            return None

    @font_size.setter
    def font_size(self, font_size: float):
        self._char['size'] = font_size

    @property
    def font_style(self):
        if 'style' in self._char:
            return self._char['style']
        else:
            return None

    @font_style.setter
    def font_style(self, font_style: str):
        self._char['style'] = font_style

    @property
    def width(self):
        if 'w' in self._char:
            return self._char['w']
        else:
            return None

    @width.setter
    def width(self, width: float):
        self._char['w'] = width

    @property
    def data(self):
        if 'data' in self._char:
            return self._char['data']
        else:
            return None

    @data.setter
    def data(self, data):
        self._data['data'] = data
        self._char['data'] = data
