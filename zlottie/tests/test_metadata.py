from unittest import TestCase
from zlottie.objects import Metadata


class TestMetadata(TestCase):
    def test_create(self):
        # arrange/act
        uut = Metadata(author='Boaz', keywords=['a', 'b'], description='test', theme_color='blue', generator='zlottie')
        # assert
        self.assertEqual(uut.author, 'Boaz')  # tag 'a'
        self.assertEqual(uut.keywords, ['a', 'b'])  #
        self.assertEqual(uut.description, 'test')
        self.assertEqual(uut.theme_color, 'blue')
        self.assertEqual(uut.generator, 'zlottie')

    def test_load(self):
        raw = {'a': 'author', 'k': ['keyword_1', 'keyword_2'], 'd': 'description', 'tc': 'theme_color', 'g': 'generator'}
        uut = Metadata()
        uut.load()
        print('asf')
