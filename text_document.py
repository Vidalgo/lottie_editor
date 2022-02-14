import enum
import copy


class Text_justify(enum.Enum):
    Left = 0
    Right = 1
    Center = 2
    JustifyWithLastLineLeft = 3
    JustifyWithLastLineRight = 4
    JustifyWithLastLineCenter = 5
    JustifyWithLastLineFull = 6


class Text_caps(enum.Enum):
    Regular = 0
    All_caps = 1
    Small_caps = 2



class text_document:
    def __init__(self, time: float = 0, font_family: str = "Arimo-Bold", font_color=None,
                 justification: Text_justify = Text_justify.Left, line_height: float = 36, font_size: float = 36,
                 text: str = "Place Text Here", text_tracking: float = 0, text_caps: Text_caps = Text_caps.Regular):
        self._text_document = {'s': {}, 't': 0.0}
        self.time = time
        self.font_family = font_family
        self.font_color = font_color
        self.justification = justification
        self.line_height = line_height
        self.font_size = font_size
        self.text = text
        self.text_tracking = text_tracking

    def analyze(self):
        if type(self._text_document) is not dict:
            raise TypeError("Error: textbox is not of type dictionary")
        if 's' not in self._text_document or 't' not in self._text_document or type(self._text_document['s']) is not dict:
            raise TypeError("Error: textbox is of bad structure or type")
        if self.time is None:
            raise TypeError("Error: textbox doesn't have correct a time member")
        if self.font_family is None:
            raise TypeError("Error: textbox doesn't have a font")
        if self.text is None:
            raise TypeError("Error: textbox doesn't have a text")
        if self.font_color is None or type(self.font_color) is not list or len(self.font_color) != 3 or \
                all(0 <= color <= 1 for color in self.font_color):
            raise TypeError("Error: textbox doesn't have a color or type or values are incorrect")

    def load(self, textbox: dict):
        self._text_document = textbox
        self.analyze()

    def copy(self, textbox: dict):
        self._text_document = copy.deepcopy(textbox)
        self.analyze()

    @property
    def text_document(self):
        return self._text_document

    @text_document.setter
    def text_document(self, text_doc: dict):
        self._text_document = text_doc
        self.analyze()

    @property
    def time(self):
        if 't' in self._text_document:
            return self._text_document['t']
        else:
            return None

    @time.setter
    def time(self, time: float):
        self._text_document['t'] = time

    @property
    def font_family(self):
        if 'f' in self._text_document['s']:
            return self._text_document['s']['f']
        else:
            return None

    @font_family.setter
    def font_family(self, font: str):
        self._text_document['s']['f'] = font

    @property
    def font_color(self):
        if 'fc' in self._text_document['s']:
            return self._text_document['s']['fc']
        else:
            return None

    @font_color.setter
    def font_color(self, font_color: list[float]):
        self._text_document['s']['fc'] = [0.5, 0.5, 0.5] if font_color is None else font_color

    @property
    def justification(self):
        if 'j' in self._text_document['s']:
            return self._text_document['s']['j']
        else:
            return None

    @justification.setter
    def justification(self, justification: Text_justify):
        self._text_document['s']['j'] = justification.value

    @property
    def line_height(self):
        if 'lh' in self._text_document['s']:
            return self._text_document['s']['lh']
        else:
            return None

    @line_height.setter
    def line_height(self, line_height: float):
        self._text_document['s']['lh'] = line_height

    @property
    def font_size(self):
        if 's' in self._text_document['s']:
            return self._text_document['s']['s']
        else:
            return None

    @font_size.setter
    def font_size(self, font_size: float):
        self._text_document['s']['s'] = font_size

    @property
    def text(self):
        if 't' in self._text_document['s']:
            return self._text_document['s']['t']
        else:
            return None

    @text.setter
    def text(self, string_value: str):
        self._text_document['s']['t'] = string_value

    @property
    def text_tracking(self):
        if 'tr' in self._text_document['s']:
            return self._text_document['s']['tr']
        else:
            return None

    @text_tracking.setter
    def text_tracking(self, tracking: float):
        self._text_document['s']['tr'] = tracking

    @property
    def text_caps(self):
        if 'j' in self._text_document['s']:
            return self._text_document['s']['ca']
        else:
            return None

    @text_caps.setter
    def text_caps(self, text_caps: Text_caps):
        self._text_document['s']['ca'] = text_caps.value
