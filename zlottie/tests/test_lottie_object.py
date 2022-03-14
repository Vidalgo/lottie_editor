from unittest import TestCase
from zlottie.tests.data.test_lottie_object import *
from zlottie.base import LottieObject, LottieAttribute
from typing import List, Optional


class TestLottieObject(TestCase):
    def setUp(self) -> None:
        self.dummy_animation_instance = DummyAnimation(
            attr1=DummyEnum.E1,
            attr2=DummyLottieObjectWithoutInit(attr1='2', attr2=22, attr3=['231', '232']),
            attr3=[
                DerivedDummyLottieObjectWithoutInit(attr1='311', attr2=321, attr3=3311, attr4=1.0),
                DerivedDummyLottieObjectWithoutInit(attr1='312', attr2=322, attr3=3321, attr4=2.0)
            ])

        self.dummy_animation_raw = {
            "a1": 1,
            "a2": {"a1": "2", "a2": 22, "a3": ["231", "232"]},
            "a3": [
                {"a1": "311", "a2": 321, "x3": 3311, "a4": 1.0},
                {"a1": "312", "a2": 322, "x3": 3321, "a4": 2.0}
            ]}

    def test_object_without_init_attributes_created(self):
        # arrange
        expected_descriptor = {
            'attr1': LottieAttribute(name='attr1', tag='a1', annotation=str),
            'attr2': LottieAttribute(name='attr2', tag='a2', annotation=Optional[int]),
            'attr3': LottieAttribute(name='attr3', tag='a3', annotation=List[str])
        }
        expected_attributes = {
            'attr1': None,
            'attr2': None,
            'attr3': None
        }
        # act
        uut = DummyLottieObjectWithoutInit()
        # assert
        self.assertIsNone(uut.attr1)
        self.assertIsNone(uut.attr2)
        self.assertIsNone(uut.attr3)
        self.assertEqual(uut.descriptor, expected_descriptor)
        self.assertEqual(uut.attributes, expected_attributes)

    def test_object_without_init_autoinit(self):
        # arrange
        expected_descriptor = {
            'attr1': LottieAttribute(name='attr1', tag='a1', annotation=str),
            'attr2': LottieAttribute(name='attr2', tag='a2', annotation=Optional[int]),
            'attr3': LottieAttribute(name='attr3', tag='a3', annotation=List[str])
        }
        expected_attributes = {
            'attr1': 'hello',
            'attr2': 2,
            'attr3': None
        }
        # act
        uut = DummyLottieObjectWithoutInit(attr1='hello', attr2=2)
        # assert
        self.assertEqual(uut.attr1, 'hello')
        self.assertEqual(uut.attr2, 2)
        self.assertIsNone(uut.attr3)
        self.assertEqual(uut.descriptor, expected_descriptor)
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
        expected_descriptor = {
            'attr1': LottieAttribute(name='attr1', tag='a1', annotation=str),
            'attr2': LottieAttribute(name='attr2', tag='a2', annotation=Optional[int]),
            'attr3': LottieAttribute(name='attr3', tag='x3', annotation=int),
            'attr4': LottieAttribute(name='attr4', tag='a4', annotation=float)
        }
        # act
        uut = DerivedDummyLottieObjectWithoutInit()
        # assert
        self.assertIsNone(uut.attr1)
        self.assertIsNone(uut.attr2)
        self.assertIsNone(uut.attr3)
        self.assertIsNone(uut.attr4)
        self.assertEqual(uut.descriptor, expected_descriptor)

    def test_derived_twice_object_attributes_created(self):
        # arrange
        expected_descriptor = {
            'attr1': LottieAttribute(name='attr1', tag='a1', annotation=str),
            'attr2': LottieAttribute(name='attr2', tag='a2', annotation=Optional[int]),
            'attr3': LottieAttribute(name='attr3', tag='x3', annotation=int),
            'attr4': LottieAttribute(name='attr4', tag='a4', annotation=float),
            'attr5': LottieAttribute(name='attr5', tag='a5', annotation=bool)
        }
        expected_tags = ['a1', 'a2', 'x3', 'a4', 'a5']
        # act
        uut = DerivedTwiceDummyLottieObjectWithoutInit(attr1='hello', attr3=1, attr5=True)
        # assert
        self.assertEqual(uut.attr1, 'hello')
        self.assertIsNone(uut.attr2)
        self.assertEqual(uut.attr3, 1)
        self.assertIsNone(uut.attr4)
        self.assertEqual(uut.attr5, True)
        self.assertEqual(uut.descriptor, expected_descriptor)
        self.assertEqual(uut.tags, expected_tags)

    def test_derived_multiple_object_attributes_created(self):
        # arrange
        expected_descriptor = {
            'attr1': LottieAttribute(name='attr1', tag='a1', annotation=int),  # taken from DummyLottieObject2, according to MRO
            'attr2': LottieAttribute(name='attr2', tag='a2', annotation=Optional[int]),
            'attr3': LottieAttribute(name='attr3', tag='a3', annotation=List[str]),
            'attr6': LottieAttribute(name='attr6', tag='a6', annotation=bool),
            'attr7': LottieAttribute(name='attr7', tag='a7', annotation=str)
        }
        expected_attributes = {
            'attr1': 'hello',
            'attr2': 2,
            'attr3': 3,
            'attr6': True,
            'attr7': 'world'
        }
        # act
        uut = DummyLottieObjectMultipleInheritance(attr1='hello', attr2=2, attr3=3, attr6=True, attr7='world')
        # assert
        self.assertEqual(uut.attr1, 'hello')
        self.assertEqual(uut.attr2, 2)
        self.assertEqual(uut.attr3, 3)
        self.assertEqual(uut.attr6, True)
        self.assertEqual(uut.attr7, 'world')
        self.assertEqual(uut.descriptor, expected_descriptor)
        self.assertEqual(uut.attributes, expected_attributes)

    def test_duplicate_tags_raise(self):
        with self.assertRaises(TypeError):
            class DummyLottieObjectDuplicateTags(DummyLottieObjectWithoutInit):
                # the tag 'a1' is already paired with DummyLottieObjectWithoutInit.attr1
                attr100: str = LottieAttribute(tag='a1')

    def test_load(self):
        # arrange
        expected = self.dummy_animation_raw
        # act
        uut = DummyAnimation()
        uut.load(raw=self.dummy_animation_raw)
        # assert
        actual = uut.to_raw()
        self.assertDictEqual(expected, actual)

    def test_from_dict(self):
        # arrange
        uut = self.dummy_animation_instance
        expected = self.dummy_animation_raw
        # act
        actual = uut.to_raw()
        # assert
        self.assertDictEqual(expected, actual)

    def test_to_dict(self):
        # arrange
        expected = self.dummy_animation_raw
        # act
        actual = DummyAnimation.from_raw(raw=self.dummy_animation_raw).to_raw()
        # assert
        self.assertDictEqual(expected, actual)

    def test_init_from_raw(self):
        # arrange
        expected = self.dummy_animation_raw
        # act
        uut = DummyAnimation(raw=self.dummy_animation_raw)
        # assert
        actual = uut.to_raw()
        self.assertDictEqual(expected, actual)
