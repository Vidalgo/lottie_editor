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


class Textbox:
    def __init__(self, time: float = 0, font: str = "Arimo-Bold", font_color: list[float] = None,
                 justification: Text_justify = Text_justify.Left, line_height: float = 36, font_size: float = 36,
                 text: str = "Place Text Here", tracking: float = 0):
        self._textbox = {'s': {}, 't': 0.0}
        self.time = time
        self.font = font
        self.font_color = font_color
        self.justification = justification
        self.line_height = line_height
        self.font_size = font_size
        self.text = text
        self.tracking = tracking

    def analyze(self):
        if type(self._textbox) is not dict:
            raise TypeError("Error: textbox is not of type dictionary")
        if 's' not in self._textbox or 't' not in self._textbox or type(self._textbox['s']) is not dict:
            raise TypeError("Error: textbox is of bad structure or type")
        if self.time is None:
            raise TypeError("Error: textbox doesn't have correct a time member")
        if self.font is None:
            raise TypeError("Error: textbox doesn't have a font")
        if self.text is None:
            raise TypeError("Error: textbox doesn't have a text")
        if self.font_color is None or type(self.font_color) is not list or len(self.font_color) != 3:
            raise TypeError("Error: textbox doesn't have a color ot type is incorrect")

    def load(self, textbox: dict):
        self._textbox = textbox
        self.analyze()

    def copy(self, textbox: dict):
        self._textbox = copy.deepcopy(textbox)
        self.analyze()

    @property
    def textbox(self):
        return self._textbox

    @textbox.setter
    def textbox(self, textbox: dict):
        self._textbox = textbox
        self.analyze()

    @property
    def time(self):
        if 't' in self._textbox:
            return self._textbox['t']
        else:
            return None

    @time.setter
    def time(self, time: float):
        self._textbox['t'] = time

    @property
    def font(self):
        if 'f' in self._textbox['s']:
            return self._textbox['s']['f']
        else:
            return None

    @font.setter
    def font(self, font: str):
        self._textbox['s']['f'] = font

    @property
    def font_color(self):
        if 'fc' in self._textbox['s']:
            return self._textbox['s']['fc']
        else:
            return None

    @font_color.setter
    def font_color(self, font_color: list[float]):
        self._textbox['s']['fc'] = [0.5, 0.5, 0.5] if font_color is None else font_color

    @property
    def justification(self):
        if 'j' in self._textbox['s']:
            return self._textbox['s']['j']
        else:
            return None

    @justification.setter
    def justification(self, justification: Text_justify):
        self._textbox['s']['j'] = justification.value

    @property
    def line_height(self):
        if 'lh' in self._textbox['s']:
            return self._textbox['s']['lh']
        else:
            return None

    @line_height.setter
    def line_height(self, line_height: float):
        self._textbox['s']['lh'] = line_height

    @property
    def font_size(self):
        if 's' in self._textbox['s']:
            return self._textbox['s']['s']
        else:
            return None

    @font_size.setter
    def font_size(self, font_size: float):
        self._textbox['s']['s'] = font_size

    @property
    def text(self):
        if 't' in self._textbox['s']:
            return self._textbox['s']['t']
        else:
            return None

    @text.setter
    def text(self, string_value: str):
        self._textbox['s']['t'] = string_value

    @property
    def tracking(self):
        if 'tr' in self._textbox['s']:
            return self._textbox['s']['tr']
        else:
            return None

    @tracking.setter
    def tracking(self, tracking: float):
        self._textbox['s']['tr'] = tracking
