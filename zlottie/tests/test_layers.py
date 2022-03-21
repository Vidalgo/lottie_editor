from unittest import TestCase
from zlottie.base import LottieObject, LottieAttribute
from zlottie.enums import LayerType
from zlottie.objects.layers import *
from typing import List


class StubLottieObject(LottieObject):
    layers: List[Layer] = LottieAttribute(tag='layers')


class TestLayer(TestCase):
    layer_types = {
        0: PrecompositionLayer,
        1: SolidColorLayer,
        2: ImageLayer,
        3: NullLayer,
        4: ShapeLayer,
        5: TextLayer,
        6: AudioLayer
    }

    def test_init_correct_layer_type(self):
        # arrange
        raw = {'layers': [{'ty': ty} for ty in self.layer_types.keys()]}
        expected = list(t for t in self.layer_types.values())
        # act
        obj = StubLottieObject()
        obj.load(raw=raw)
        # assert
        actual = [type(layer) for layer in obj.layers]
        self.assertSequenceEqual(actual, expected)
