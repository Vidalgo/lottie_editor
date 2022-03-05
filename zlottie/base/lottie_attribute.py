from typing import ForwardRef, Any

LottieAttribute = ForwardRef('LottieAttribute')


class LottieAttribute:
    def __init__(self, tag: str = None, type: Any = None, description: str = '', **kwargs):
        self.tag = tag
        self.type = type
        self.description = description

    def clone(self, **kwargs):
        attrs = vars(self)
        attrs.update(kwargs)
        obj = type(self)(**attrs)
        return obj

    def __repr__(self):
        return f'<LottieAttribute ("{self.tag}")>'
