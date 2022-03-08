from unittest import TestCase
from zlottie.base import LottieAttribute
from typing import List


class TestLottieAttribute(TestCase):
    def test_simple_annotation(self):
        uut = LottieAttribute(annotation=str)
        self.assertEqual(str, uut.annotation)
        self.assertFalse(uut.is_optional)
        self.assertFalse(uut.is_list)
        self.assertEqual(str, uut.type)

    def test_simple_list(self):
        uut = LottieAttribute(annotation=list[str])
        self.assertEqual(list[str], uut.annotation)
        self.assertFalse(uut.is_optional)
        self.assertTrue(uut.is_list)
        self.assertEqual(str, uut.type)

    def test_annotation_list(self):
        uut = LottieAttribute(annotation=List[str])
        self.assertEqual(List[str], uut.annotation)
        self.assertFalse(uut.is_optional)
        self.assertTrue(uut.is_list)
        self.assertEqual(str, uut.type)
