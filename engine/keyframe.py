import copy


class Keyframe:
    def __init__(self, time: float = 0, hold: int = 0, in_tangent=None, out_tangent=None, value=None):
        self._keyframe = {}
        self.time = time
        self.hold = hold
        self.in_tangent = in_tangent
        self.out_tangent = out_tangent
        self.value = value

    def analyze(self):
        if type(self._keyframe) is not dict:
            raise TypeError("Error: animated property is not of type dictionary")
        if self.time is None:
            raise TypeError("Error: keyframe  doesn't have a time property")
        if self.value is None:
            raise TypeError("Error: keyframe  doesn't have a value property")

    def load(self, keyframe: dict):
        self._keyframe = keyframe
        self.analyze()

    def copy(self, keyframe: dict):
        self._keyframe = copy.deepcopy(keyframe)
        self.analyze()

    @property
    def keyframe(self):
        return self._keyframe

    @keyframe.setter
    def keyframe(self, keyframe: dict):
        self._keyframe = keyframe
        self.analyze()

    @property
    def time(self):
        if 't' in self._keyframe:
            return self._keyframe['t']
        else:
            return 0

    @time.setter
    def time(self, time: float):
        self._keyframe['t'] = time

    @property
    def in_tangent(self):
        if 'i' in self._keyframe:
            return self._keyframe['i']
        else:
            return 0

    @in_tangent.setter
    def in_tangent(self, in_tangent: dict):
        self._keyframe['i'] = in_tangent

    @property
    def out_tangent(self):
        if 'o' in self._keyframe:
            return self._keyframe['o']
        else:
            return 0

    @out_tangent.setter
    def out_tangent(self, out_tangent: dict):
        self._keyframe['o'] = out_tangent
