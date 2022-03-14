from unittest import TestCase
from zlottie.objects import Animation
from pathlib import Path
import json


class TestAnimation(TestCase):
    _lotties_path = Path(__file__).parent / 'data/lotties'

    def setUp(self) -> None:
        with open(self._lotties_path / 'coin.json') as f:
            self.raw = json.load(f)

    def test_load(self):
        # test that load() does not raise
        uut = Animation()
        uut.load(raw=self.raw)

    def test_init(self):
        # test that load() does not raise
        uut = Animation(self.raw)

    def test_to_dict(self):
        # arrange
        uut = Animation()
        uut.load(raw=self.raw)
        # act
        actual = uut.dump()
        # assert
        self.assertDictEqual(self.raw, actual)

