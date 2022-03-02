from engine.text_transform import Text_transform
from engine.text_document import text_document
import copy


class Text_animator_data:
    def __init__(self, animators=None, text_more_option=None, masked_path: float = 0, text_boxes=None):
        self._text_animator_data = {'a': [], 'd': {'k': []}, 'm': {'a': {'a': 0, 'k': [0, 0], "ix": 2}}, 'p': {}}
        self._text_boxes: list[text_document] = []
        self._animators = []
        self.animators = animators
        self.text_more_option = text_more_option
        self.masked_path = masked_path
        self.text_boxes = text_boxes

    def analyze(self):
        if type(self._text_animator_data) is not dict:
            raise TypeError("Error: textdata is not of type dictionary")
        if 'a' not in self._text_animator_data or 'd' not in self._text_animator_data or 'k' not in self._text_animator_data['d'] or \
                'm' not in self._text_animator_data or 'p' not in self._text_animator_data:
            raise TypeError("Error: textdata is of bad structure or type")
        if self.text_boxes is None:
            raise TypeError("Error: textdata doesn't have a textbox")

    def load(self, text_animator_data: dict):
        self._text_boxes = []
        self._text_animator_data = text_animator_data
        self.analyze()
        for lottie_textbox in text_animator_data['d']['k']:
            textbox = text_document()
            textbox.load(lottie_textbox)
            self._text_boxes.append(textbox)

    def copy(self, text_animator_data: dict):
        self._text_animator_data = copy.deepcopy(text_animator_data)
        self.analyze()

    @property
    def text_animator_data(self):
        return self._text_animator_data

    @text_animator_data.setter
    def text_animator_data(self, text_animator_data: dict):
        self._text_animator_data = text_animator_data
        self.analyze()

    @property
    def animators(self):
        return self._animators

    @animators.setter
    def animators(self, animators: list[Text_transform]):
        self._animators = animators
        self._text_animator_data['a'] = [] if animators is None else [animator.transform for animator in animators]

    def add_animator(self, animator: Text_transform):
        self._animators += animator
        self._text_animator_data['a'] += animator.transform

    def delete_animator(self, animator: Text_transform):
        self._animators.remove(animator)
        self._text_animator_data['a'].remove(animator.transform)

    @property
    def text_boxes(self):
        if 'd' in self._text_animator_data and 'k' in self._text_animator_data['d']:
            return self._text_boxes
        else:
            return None

    @text_boxes.setter
    def text_boxes(self, text_boxes: list[text_document]):
        if text_boxes is None:
            textbox = text_document()
            self.__add__(textbox)
        else:
            self._text_boxes = text_boxes
            if 'k' not in self._text_animator_data['d']:
                self._text_animator_data['d']['k'] = []
            self._text_animator_data['d']['k'] = [textbox.text_document for textbox in text_boxes]

    def __add__(self, textbox: text_document):
        self._text_boxes.append(textbox)
        if 'k' not in self._text_animator_data['d']:
            self._text_animator_data['d']['k'] = []
        self._text_animator_data['d']['k'].append(textbox.text_document)

    '''def add_textbox(self, textbox: Textbox):
        self._text_boxes.append(textbox)
        if 'k' not in self._textdata['d']:
            self._textdata['d']['k'] = []
        self._textdata['d']['k'].append(textbox._textbox)'''

    def remove_textbox(self, textbox: text_document):
        self._text_boxes.remove(textbox)
        self._text_animator_data['d']['k'].remove(textbox.text_document)

    @property
    def text(self):
        return self._text_boxes[0].text

    @text.setter
    def text(self, text):
        self._text_boxes[0].text = text
