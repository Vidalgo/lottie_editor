from vidalgo_lottie_base import Vidalgo_lottie_base


class Char(Vidalgo_lottie_base):
    def __init__(self, character: str = None, font_family: str = None, font_size: float = 0,
                 font_style: str = "normal", width: float = 0, data=None):
        super(Char, self).__init__()
        self._data = {}
        self.character = character
        self.font_family = font_family
        self.font_size = font_size
        self.font_style = font_style
        self.width = width
        self.data = data

    def analyze(self):
        super(Char, self).analyze()
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

    def load(self, char: dict):
        self.lottie_base = char
        # self.data.load(char['data'])
        self.analyze()

    def copy(self, font: dict):
        super(Char, self).copy()
        self.analyze()

    @property
    def char(self):
        return self.lottie_base

    @char.setter
    def char(self, char):
        self.lottie_base = char
        self.analyze()

    @property
    def character(self):
        if 'ch' in self.lottie_base:
            return self.lottie_base['ch']
        else:
            return None

    @character.setter
    def character(self, ascent: character):
        self.lottie_base['ch'] = ascent

    @property
    def font_family(self):
        if 'fFamily' in self.lottie_base:
            return self.lottie_base['fFamily']
        else:
            return None

    @font_family.setter
    def font_family(self, font_family: str):
        self.lottie_base['fFamily'] = font_family

    @property
    def font_size(self):
        if 'size' in self.lottie_base:
            return self.lottie_base['size']
        else:
            return None

    @font_size.setter
    def font_size(self, font_size: float):
        self.lottie_base['size'] = font_size

    @property
    def font_style(self):
        if 'style' in self.lottie_base:
            return self.lottie_base['style']
        else:
            return None

    @font_style.setter
    def font_style(self, font_style: str):
        self.lottie_base['style'] = font_style

    @property
    def width(self):
        if 'w' in self.lottie_base:
            return self.lottie_base['w']
        else:
            return None

    @width.setter
    def width(self, width: float):
        self.lottie_base['w'] = width

    @property
    def data(self):
        if 'data' in self.lottie_base:
            return self.lottie_base['data']
        else:
            return None

    @data.setter
    def data(self, data):
        self._data['data'] = data
        self.lottie_base['data'] = data
