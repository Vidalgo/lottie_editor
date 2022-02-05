from text_transform import Text_transform
from textbox import Textbox
import copy


class Textdata:
    def __init__(self, animators: Text_transform = None, more_option=None, path: float = 0, text_boxes: list[Textbox] = None):
        self._textdata = {'a': [], 'd': {'k': []}, 'm': {'a': {'a': 0, 'k': [0, 0], "ix": 2}}, 'p': {}}
        self._text_boxes: list[Textbox] = []
        self._animators = []
        self.animators = animators
        self.more_option = more_option
        self.path = path
        self.text_boxes = text_boxes

    def analyze(self):
        if type(self._textdata) is not dict:
            raise TypeError("Error: textdata is not of type dictionary")
        if 'a' not in self._textdata or 'd' not in self._textdata or 'k' not in self._textdata['d'] or \
                'm' not in self._textdata or 'p' not in self._textdata:
            raise TypeError("Error: textdata is of bad structure or type")
        if self.text_boxes is None:
            raise TypeError("Error: textdata doesn't have a textbox")

    def load(self, textdata: dict):
        self._text_boxes = []
        self._textdata = textdata
        self.analyze()
        for lottie_textbox in textdata['d']['k']:
            textbox = Textbox()
            textbox.load(lottie_textbox)
            self._text_boxes.append(textbox)

    def copy(self, textdata: dict):
        self._textdata = copy.deepcopy(textdata)
        self.analyze()

    @property
    def textdata(self):
        return self._textdata

    @textdata.setter
    def textdata(self, textdata: dict):
        self._textdata = textdata
        self.analyze()

    @property
    def animators(self):
        return self._animators

    @animators.setter
    def animators(self, animators: list[Text_transform]):
        self._animators = animators
        self._textdata['a'] = [] if animators is None else [animator.transform for animator in animators]

    def add_animator(self, animator: Text_transform):
        self._animators += animator
        self._textdata['a'] += animator.transform

    def delete_animator(self, animator: Text_transform):
        self._animators.remove(animator)
        self._textdata['a'].remove(animator.transform)

    @property
    def text_boxes(self):
        if 'd' in self._textdata and 'k' in self._textdata['d']:
            return self._text_boxes
        else:
            return None

    @text_boxes.setter
    def text_boxes(self, text_boxes: list[Textbox]):
        if text_boxes is None:
            textbox = Textbox()
            self.__add__(textbox)
        else:
            self._text_boxes = text_boxes
            if 'k' not in self._textdata['d']:
                self._textdata['d']['k'] = []
            self._textdata['d']['k'] = [textbox.textbox for textbox in text_boxes]

    def __add__(self, textbox: Textbox):
        self._text_boxes.append(textbox)
        if 'k' not in self._textdata['d']:
            self._textdata['d']['k'] = []
        self._textdata['d']['k'].append(textbox.textbox)

    '''def add_textbox(self, textbox: Textbox):
        self._text_boxes.append(textbox)
        if 'k' not in self._textdata['d']:
            self._textdata['d']['k'] = []
        self._textdata['d']['k'].append(textbox._textbox)'''

    def remove_textbox(self, textbox: Textbox):
        self._text_boxes.remove(textbox)
        self._textdata['d']['k'].remove(textbox.textbox)

    @property
    def text(self):
        return self._text_boxes[0].text

    @text.setter
    def text(self, text):
        self._text_boxes[0].text = text
