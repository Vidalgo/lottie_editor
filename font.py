import enum
import copy


class Font_origin(enum.Enum):
    Local = 0
    CssUrl = 1
    ScriptUrl = 2
    FontUrl = 3


class Font:
    def __init__(self, ascent: float = 75, font_family: str = "Arimo", font_name: str = "Arimo-Bold",
                 font_style: str = "normal", font_path: str = None, font_weight: str = "normal",
                 origin: Font_origin = None, font_class: str = None):
        self.font = {}
        self.ascent = ascent
        self.font_family = font_family
        self.font_name = font_name
        self.font_style = font_style
        self.font_path = font_path
        self.character_data = font_weight
        self.origin = origin
        self.font_class = font_class
        self.analyze()

    def analyze(self):
        pass

    def load(self, font: dict):
        self.font = font
        self.analyze()

    def copy(self, font: dict):
        self.font = copy.deepcopy(font)
        self.analyze()

    @property
    def ascent(self):
        if 'ascent' in self.font:
            return self.font['ascent']
        else:
            return None

    @ascent.setter
    def ascent(self, ascent: float):
        self.font['ascent'] = ascent

    @property
    def font_family(self):
        if 'fFamily' in self.font:
            return self.font['fFamily']
        else:
            return None

    @font_family.setter
    def font_family(self, font_family: str):
        self.font['fFamily'] = font_family

    @property
    def font_name(self):
        if 'fName' in self.font:
            return self.font['fName']
        else:
            return None

    @font_name.setter
    def font_name(self, font_name: str):
        self.font['fName'] = font_name

    @property
    def font_style(self):
        if 'fStyle' in self.font:
            return self.font['fStyle']
        else:
            return None

    @font_style.setter
    def font_style(self, font_style: str):
        self.font['fStyle'] = font_style

    @property
    def font_path(self):
        if 'fPath' in self.font:
            return self.font['fPath']
        else:
            return None

    @font_path.setter
    def font_path(self, font_path: str):
        self.font['fPath'] = font_path

    @property
    def font_weight(self):
        if 'fWeight' in self.font:
            return self.font['fWeight']
        else:
            return None

    @font_weight.setter
    def font_weight(self, font_weight: str):
        self.font['fWeight'] = font_weight

    @property
    def origin(self):
        if 'origin' in self.font:
            return self.font['origin']
        else:
            return None

    @origin.setter
    def origin(self, origin: Font_origin):
        self.font['origin'] = origin

    @property
    def font_class(self):
        if 'fClass' in self.font:
            return self.font['fClass']
        else:
            return None

    @font_class.setter
    def font_class(self, font_class: str):
        self.font['fClass'] = font_class

