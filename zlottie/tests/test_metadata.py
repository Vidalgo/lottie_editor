from unittest import TestCase
from zlottie.objects import Metadata
from dataclasses import dataclass


class TestMetadata(TestCase):
    def test_create(self):
        # arrange/act
        uut = Metadata(author='Boaz', keywords=['a', 'b'], description='test', theme_color='blue', generator='zlottie')
        # assert
        self.assertEqual(uut.author, 'Boaz')
        self.assertEqual(uut.keywords, ['a', 'b'])
        self.assertEqual(uut.description, 'test')
        self.assertEqual(uut.theme_color, 'blue')
        self.assertEqual(uut.generator, 'zlottie')
