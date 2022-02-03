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


class Text_keyframe:
    def __init__(self, time: float = 0, font: str = "Arimo-Bold", font_color: list[float] = None,
                 justification: Text_justify = Text_justify.Left, line_height: float = 36, font_size: float = 36,
                 string_value: str = "Place Text Here", tracking: float = 0):
        self.text_keyframe = {'s': {}}
        self.time = time
        self.font = font
        self.font_color = font_color
        self.justification = justification
        self.line_height = line_height
        self.font_size = font_size
        self.string_value = string_value
        self.tracking = tracking
        self.analyze()

    def analyze(self):
        pass

    def load(self, text_keyframe: dict):
        self.text_keyframe = text_keyframe
        self.analyze()

    def copy(self, text_keyframe: dict):
        self.text_keyframe = copy.deepcopy(text_keyframe)
        self.analyze()

    @property
    def time(self):
        if 't' in self.text_keyframe:
            return self.text_keyframe['t']
        else:
            return None

    @time.setter
    def time(self, time: str):
        self.text_keyframe['t'] = time

    @property
    def font(self):
        if 'f' in self.text_keyframe['s']:
            return self.text_keyframe['s']['f']
        else:
            return None

    @font.setter
    def font(self, font: str):
        self.text_keyframe['s']['f'] = font

    @property
    def font_color(self):
        if 'fc' in self.text_keyframe['s']:
            return self.text_keyframe['s']['fc']
        else:
            return None

    @font_color.setter
    def font_color(self, font_color: list[float]):
        self.text_keyframe['s']['fc'] = [0.5, 0.5, 0.5] if font_color is None else font_color

    @property
    def justification(self):
        if 'j' in self.text_keyframe['s']:
            return self.text_keyframe['s']['j']
        else:
            return None

    @justification.setter
    def justification(self, justification: Text_justify):
        self.text_keyframe['s']['j'] = justification.value

    @property
    def line_height(self):
        if 'lh' in self.text_keyframe['s']:
            return self.text_keyframe['s']['lh']
        else:
            return None

    @line_height.setter
    def line_height(self, line_height: float):
        self.text_keyframe['s']['lh'] = line_height

    @property
    def font_size(self):
        if 's' in self.text_keyframe['s']:
            return self.text_keyframe['s']['s']
        else:
            return None

    @font_size.setter
    def font_size(self, font_size: float):
        self.text_keyframe['s']['s'] = font_size

    @property
    def string_value(self):
        if 't' in self.text_keyframe['s']:
            return self.text_keyframe['s']['t']
        else:
            return None

    @string_value.setter
    def string_value(self, string_value: str):
        self.text_keyframe['s']['t'] = string_value

    @property
    def tracking(self):
        if 'tr' in self.text_keyframe['s']:
            return self.text_keyframe['s']['tr']
        else:
            return None

    @tracking.setter
    def tracking(self, tracking: float):
        self.text_keyframe['s']['tr'] = tracking
