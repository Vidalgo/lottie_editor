from text_document import Text_properties


class Text_keyframes:
    def __init__(self, animators: list = None, more_option=None, path: float = 0, document_data=None):
        self.text_keyframe = {}
        self._animators: list[Text_transform] = list()
        self.animators = animators
        self.more_option = more_option
        self.path = path
        self.document_data = document_data
        self.analyze()

    def analyze(self):
        pass

    @property
    def animators(self):
        return self._animators

    @animators.setter
    def animators(self, animators: list[Text_transform]):
        self._animators = animators
        self.text_data['a'] = None if animators is None else [animator.transform for animator in animators]
