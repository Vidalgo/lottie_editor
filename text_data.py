from text_transform import Text_transform
from text_keyframe import Text_keyframe


class Text_data:
    def __init__(self, animators: Text_transform = None, more_option=None, path: float = 0,
                 string_data: list[Text_keyframe] = None):
        self.text_data = {'a': [], 'd': {}, 'm': {'a': {'a': 0, 'k': [0, 0], "ix": 2}}, 'p': {}}
        self._animators = []
        self._text_keyframe = []
        self.animators = animators
        self.more_option = more_option
        self.path = path
        self.string_data = string_data
        self.analyze()

    def analyze(self):
        pass

    def load(self, text_data: dict):
        self.text_data = text_data

    @property
    def animators(self):
        return self._animators

    @animators.setter
    def animators(self, animators: list[Text_transform]):
        self._animators = animators
        self.text_data['a'] = [] if animators is None else [animator.transform for animator in animators]

    def add_animator(self, animator: Text_transform):
        self._animators += animator
        self.text_data['a'] += animator.transform

    def delete_animator(self, animator: Text_transform):
        self._animators.remove(animator)
        self.text_data['a'].remove(animator.transform)

    @property
    def string_data(self):
        return self._text_keyframe

    @string_data.setter
    def string_data(self, string_data_items: list[Text_keyframe]):
        if string_data_items is None:
            string_data = Text_keyframe()
            self.add_string(string_data)
        else:
            self._text_keyframe = string_data_items
            self.text_data['d']['k'] = [string_data.text_keyframe for string_data in string_data_items]

    def add_string(self, string_data: Text_keyframe):
        self._text_keyframe.append(string_data)
        if 'k' not in self.text_data['d']:
            self.text_data['d']['k'] = []
        self.text_data['d']['k'].append(string_data.text_keyframe)

    def delete_string(self, string_data: Text_keyframe):
        self._text_keyframe.remove(string_data)
        self.text_data['d']['k'].remove(string_data.text_keyframe)
