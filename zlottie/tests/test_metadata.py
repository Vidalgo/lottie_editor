from unittest import TestCase
from zlottie.objects import Metadata


class TestMetadata(TestCase):
    def setUp(self) -> None:
        self.raw = {
            'a': 'author',
            'k': ['keyword_1', 'keyword_2'],
            'd': 'description',
            'tc': 'theme_color',
            'g': 'generator'
        }

    def test_create(self):
        # arrange/act
        uut = Metadata(author=self.raw['a'], keywords=self.raw['k'], description=self.raw['d'], theme_color=self.raw['tc'], generator=self.raw['g'])
        # assert
        self.assertEqual(uut.author, self.raw['a'])
        self.assertEqual(uut.keywords, self.raw['k'])
        self.assertEqual(uut.description, self.raw['d'])
        self.assertEqual(uut.theme_color, self.raw['tc'])
        self.assertEqual(uut.generator, self.raw['g'])

    def test_load(self):
        # act
        uut = Metadata()
        uut.load(raw=self.raw)
        # assert
        self.assertEqual('author', uut.author)
        self.assertEqual(['keyword_1', 'keyword_2'], uut.keywords)
        self.assertEqual('description', uut.description)
        self.assertEqual('theme_color', uut.theme_color)
        self.assertEqual('generator', uut.generator)

    def test_from_dict(self):
        # act
        uut = Metadata.from_raw(raw=self.raw)
        # assert
        self.assertEqual('author', uut.author)
        self.assertEqual(['keyword_1', 'keyword_2'], uut.keywords)
        self.assertEqual('description', uut.description)
        self.assertEqual('theme_color', uut.theme_color)
        self.assertEqual('generator', uut.generator)

    def test_to_dict(self):
        # arrange
        uut = Metadata.from_raw(raw=self.raw)
        # act
        raw = uut.dump()
        # assert
        self.assertDictEqual(self.raw, raw)
