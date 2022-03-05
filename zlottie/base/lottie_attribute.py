from typing import Any


class LottieAttribute:
    _eq_attrs = ['tag', 'type']

    def __init__(self, tag: str = None, type: Any = None, description: str = ''):
        self.tag = tag
        self.type = type
        self.description = description

    def clone(self, **kwargs):
        attrs = vars(self)
        attrs.update(kwargs)
        obj = type(self)(**attrs)
        return obj

    def __repr__(self):
        return f"<LottieAttribute ('{self.tag}')>"

    def __eq__(self, other):
        return all(getattr(self, attr) == getattr(other, attr) for attr in self._eq_attrs)
