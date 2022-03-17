from zlottie.base import LottieObject, LottieAttribute
from zlottie.objects import Layer
from typing import List


class Composition(LottieObject):
    layers: List[Layer] = LottieAttribute(tag='layers', description='composition layers')
