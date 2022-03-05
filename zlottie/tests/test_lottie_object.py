from unittest import TestCase
from zlottie.base import LottieObject, LottieAttribute
from typing import List, Optional


class DummyLottieObjectWithoutInit(LottieObject):
    attr1: str = LottieAttribute(tag='a1', description='required string attribute')
    attr2: Optional[int] = LottieAttribute(tag='a2', description='optional int attribute')
    attr3: List[str] = LottieAttribute(tag='a3', description='required list attribute')


class DummyLottieObjectWithInit(LottieObject):
    attr1: str = LottieAttribute(tag='a1', description='required string attribute')
    attr2: Optional[int] = LottieAttribute(tag='a2', description='optional int attribute')
    attr3: List[str] = LottieAttribute(tag='a3', description='required list attribute')

    def __init__(self, *args, **kwargs):
        self.x = kwargs.get('x', 1)


class DerivedDummyLottieObjectWithoutInit(DummyLottieObjectWithoutInit):
    # note that attr3 overrides both type and tag
    attr3: int = LottieAttribute(tag='x3', description='overrides attribute from baseclass')
    attr4: float = LottieAttribute(tag='a4', description='required string attribute')


class DerivedTwiceDummyLottieObjectWithoutInit(DerivedDummyLottieObjectWithoutInit):
    # note that attr3 overrides both type and tag
    attr5: bool = LottieAttribute(tag='a5', description='required boolean attribute')


class TestLottieObject(TestCase):
    def test_object_without_init_attributes_created(self):
        # arrange
        expected_attributes = {
            'attr1': LottieAttribute(tag='a1', type=str),
            'attr2': LottieAttribute(tag='a2', type=Optional[int]),
            'attr3': LottieAttribute(tag='a3', type=List[str])
        }
        # act
        uut = DummyLottieObjectWithoutInit()
        # assert
        self.assertIsNone(uut.attr1)
        self.assertIsNone(uut.attr2)
        self.assertIsNone(uut.attr3)
        self.assertEqual(uut.attributes, expected_attributes)

    def test_object_without_init_autoinit(self):
        # arrange
        expected_attributes = {
            'attr1': LottieAttribute(tag='a1', type=str),
            'attr2': LottieAttribute(tag='a2', type=Optional[int]),
            'attr3': LottieAttribute(tag='a3', type=List[str])
        }
        # act
        uut = DummyLottieObjectWithoutInit(attr1='hello', attr2=2)
        # assert
        self.assertEqual(uut.attr1, 'hello')
        self.assertEqual(uut.attr2, 2)
        self.assertIsNone(uut.attr3)
        self.assertEqual(uut.attributes, expected_attributes)

    def test_object_without_init_autoinit_raises(self):
        # arrange/act
        with self.assertRaises(TypeError):
            DummyLottieObjectWithoutInit(no_such_attr=2)

    def test_object_with_init_ignores_autoinit(self):
        # arrange/act
        uut = DummyLottieObjectWithInit(x=2)
        # assert
        self.assertEqual(uut.x, 2)
        self.assertIsNone(uut.attr1)
        self.assertIsNone(uut.attr2)
        self.assertIsNone(uut.attr3)

    def test_derived_object_attributes_created(self):
        # arrange
        expected_attributes = {
            'attr1': LottieAttribute(tag='a1', type=str),
            'attr2': LottieAttribute(tag='a2', type=Optional[int]),
            'attr3': LottieAttribute(tag='x3', type=int),
            'attr4': LottieAttribute(tag='a4', type=float)
        }
        # act
        uut = DerivedDummyLottieObjectWithoutInit()
        # assert
        self.assertIsNone(uut.attr1)
        self.assertIsNone(uut.attr2)
        self.assertIsNone(uut.attr3)
        self.assertIsNone(uut.attr4)
        self.assertEqual(uut.attributes, expected_attributes)

    def test_derived_twice_object_attributes_created(self):
        # arrange
        expected_attributes = {
            'attr1': LottieAttribute(tag='a1', type=str),
            'attr2': LottieAttribute(tag='a2', type=Optional[int]),
            'attr3': LottieAttribute(tag='x3', type=int),
            'attr4': LottieAttribute(tag='a4', type=float),
            'attr5': LottieAttribute(tag='a5', type=bool)
        }
        # act
        uut = DerivedTwiceDummyLottieObjectWithoutInit(attr1='hello', attr3=1, attr5=True)
        # assert
        self.assertEqual(uut.attr1, 'hello')
        self.assertIsNone(uut.attr2)
        self.assertEqual(uut.attr3, 1)
        self.assertIsNone(uut.attr4)
        self.assertEqual(uut.attr5, True)
        self.assertEqual(uut.attributes, expected_attributes)
