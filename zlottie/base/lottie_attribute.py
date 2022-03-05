from typing import ForwardRef, Any

LottieAttribute = ForwardRef('LottieAttribute')


class LottieAttribute:
    def __init__(self, tag: str = None, type: Any = None, description: str = '', **kwargs):
        self.tag = tag
        self.type = type
        self.description = description

    @classmethod
    def copy(cls, source: LottieAttribute, **kwargs):
        attrs = vars(source)
        attrs.update(kwargs)
        obj = cls(**attrs)
        return obj
