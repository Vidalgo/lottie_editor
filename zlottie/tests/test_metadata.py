from unittest import TestCase
from zlottie.objects import Metadata
from dataclasses import dataclass

class TestMetadata(TestCase):
    def test_create(self):
        m = Metadata(author='Boaz', z=1)
        print('asfd')