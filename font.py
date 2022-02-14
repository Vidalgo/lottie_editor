import enum
import copy
from helpers import generate_random_id, VIDALGO_ID

class Font_origin(enum.Enum):
    Local = 0
    CssUrl = 1
    ScriptUrl = 2
    FontUrl = 3


class Font:
    def __init__(self, ascent: float = 75, font_family: str = "Arimo", font_name: str = "Arimo-Bold",
                 font_style: str = "normal", font_path: str = None, font_weight: str = "normal",
                 origin: Font_origin = None, font_class: str = None):
        self._font = {}
        self.ascent = ascent
        self.font_family = font_family
        self.font_name = font_name
        self.font_style = font_style
        self.font_path = font_path
        self.character_data = font_weight
        self.origin = origin
        self.font_class = font_class
        generate_random_id(self._font)

    def analyze(self):
        if type(self._font) is not dict:
            raise TypeError("Error: layer is not of type dictionary")
        if self.vidalgo_id is None:
            raise TypeError("Error: font doesn't have a vidalgo id")

    def load(self, font: dict):
        self._font = font
        generate_random_id(self._font)
        self.analyze()

    def copy(self, font: dict):
        self._font = copy.deepcopy(font)
        self.analyze()

    @property
    def vidalgo_id(self):
        if VIDALGO_ID in self._font:
            return self._font[VIDALGO_ID]
        else:
            return None

    @vidalgo_id.setter
    def vidalgo_id(self, vidalgo_id: str):
        self._font[VIDALGO_ID] = vidalgo_id

    @property
    def font(self):
        return self._font

    @font.setter
    def font(self, font):
        self._font = font
        self.analyze()

    @property
    def ascent(self):
        if 'ascent' in self._font:
            return self._font['ascent']
        else:
            return None

    @ascent.setter
    def ascent(self, ascent: float):
        self._font['ascent'] = ascent

    @property
    def font_family(self):
        if 'fFamily' in self._font:
            return self._font['fFamily']
        else:
            return None

    @font_family.setter
    def font_family(self, font_family: str):
        self._font['fFamily'] = font_family

    @property
    def font_name(self):
        if 'fName' in self._font:
            return self._font['fName']
        else:
            return None

    @font_name.setter
    def font_name(self, font_name: str):
        self._font['fName'] = font_name

    @property
    def font_style(self):
        if 'fStyle' in self._font:
            return self._font['fStyle']
        else:
            return None

    @font_style.setter
    def font_style(self, font_style: str):
        self._font['fStyle'] = font_style

    @property
    def font_path(self):
        if 'fPath' in self._font:
            return self._font['fPath']
        else:
            return None

    @font_path.setter
    def font_path(self, font_path: str):
        self._font['fPath'] = font_path

    @property
    def font_weight(self):
        if 'fWeight' in self._font:
            return self._font['fWeight']
        else:
            return None

    @font_weight.setter
    def font_weight(self, font_weight: str):
        self._font['fWeight'] = font_weight

    @property
    def origin(self):
        if 'origin' in self._font:
            return self._font['origin']
        else:
            return None

    @origin.setter
    def origin(self, origin: Font_origin):
        self._font['origin'] = origin

    @property
    def font_class(self):
        if 'fClass' in self._font:
            return self._font['fClass']
        else:
            return None

    @font_class.setter
    def font_class(self, font_class: str):
        self._font['fClass'] = font_class

