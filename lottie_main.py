from image_asset import Image_asset
from precomposition import Precomposition
from layer import Layer


class Lottie_main:
    def __init__(self, main):
        self.main = main
        if type(main) is not dict:
            raise TypeError("Error: pre-composition is not of type dictionary")
        self.images = []
        self.precomp = []
        self.main_layers = []

    @property
    def name(self):
        if 'nm' in self.main:
            return self.main['nm']
        else:
            return None

    @name.setter
    def name(self, new_name):
        self.main['nm'] = new_name
