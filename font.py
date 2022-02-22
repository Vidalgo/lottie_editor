import enum
from vidalgo_lottie_base import Vidalgo_lottie_base


class Font_origin(enum.Enum):
    Local = 0
    CssUrl = 1
    ScriptUrl = 2
    FontUrl = 3


class Font(Vidalgo_lottie_base):
    def __init__(self, ascent: float = 75, font_family: str = "Arimo", font_name: str = "Arimo-Bold",
                 font_style: str = "normal", font_path: str = None, font_weight: str = "normal",
                 origin: Font_origin = None, font_class: str = None):
        super(Font, self).__init__()
        self.ascent = ascent
        self.font_family = font_family
        self.font_name = font_name
        self.font_style = font_style
        self.font_path = font_path
        self.character_data = font_weight
        self.origin = origin
        self.font_class = font_class

    def analyze(self):
        super(Font, self).analyze()

    def load(self, font: dict):
        self.lottie_base = font
        self.analyze()

    def copy(self, font: dict):
        super(Font, self).copy()
        self.refactor_id()
        self.analyze()

    @property
    def font(self):
        return self.lottie_base

    @font.setter
    def font(self, font):
        self.lottie_base = font
        self.analyze()

    @property
    def ascent(self):
        if 'ascent' in self.lottie_base:
            return self.lottie_base['ascent']
        else:
            return None

    @ascent.setter
    def ascent(self, ascent: float):
        self.lottie_base['ascent'] = ascent

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
    def font_name(self):
        if 'fName' in self.lottie_base:
            return self.lottie_base['fName']
        else:
            return None

    @font_name.setter
    def font_name(self, font_name: str):
        self.lottie_base['fName'] = ''
        self.lottie_element_id = font_name

    @property
    def font_style(self):
        if 'fStyle' in self.lottie_base:
            return self.lottie_base['fStyle']
        else:
            return None

    @font_style.setter
    def font_style(self, font_style: str):
        self.lottie_base['fStyle'] = font_style

    @property
    def font_path(self):
        if 'fPath' in self.lottie_base:
            return self.lottie_base['fPath']
        else:
            return None

    @font_path.setter
    def font_path(self, font_path: str):
        self.lottie_base['fPath'] = font_path

    @property
    def font_weight(self):
        if 'fWeight' in self.lottie_base:
            return self.lottie_base['fWeight']
        else:
            return None

    @font_weight.setter
    def font_weight(self, font_weight: str):
        self.lottie_base['fWeight'] = font_weight

    @property
    def origin(self):
        if 'origin' in self.lottie_base:
            return self.lottie_base['origin']
        else:
            return None

    @origin.setter
    def origin(self, origin: Font_origin):
        self.lottie_base['origin'] = origin

    @property
    def font_class(self):
        if 'fClass' in self.lottie_base:
            return self.lottie_base['fClass']
        else:
            return None

    @font_class.setter
    def font_class(self, font_class: str):
        self.lottie_base['fClass'] = font_class

