from lottie_search_and_replace import load_json, store_json
from image import Image
from precomp import Precomp
from layer import Layer

PATH = "/lottie_files_path/"

class Lottie_animation:
    def __init__(self):
        self.main = dict
        self.assets = None
        self.fonts = None
        self.chars = None
        self.markers = None
        self.layers = list[Layer]

    def load(self, animation_file_name):
        self.main = load_json(animation_file_name)
        self.analyze()

    def store(self, file_name = None):
        if file_name is None:
            file_name = "{0}{1}.json".format(PATH, self.name)
        store_json(file_name, self.main)

    def create(self, lottie_name : str, in_point : int = 1, out_point: int = 30, frame_rate: int = 30,
               ddd_layers : int = 0, width : float = 500, height : float = 500):
        self.name = lottie_name
        self.width = width
        self.height = height
        self.frame_rate = frame_rate
        self.in_point = in_point
        self.out_point = out_point
        self.ddd_layers = ddd_layers
        self.assets = []
        self.fonts = {}
        self.chars = []
        self.markers = []
        self.layers = []

        pass

    def analyze(self):
        if type(self.main) is not dict:
            raise TypeError("Error: composition is not of type dictionary")
        if self.name is None:
            raise TypeError("Error: composition doesn't have a name")
        if self.in_point is None:
            raise TypeError("Error: initial Frame of the animation is not set")
        if self.out_point is None:
            raise TypeError("Error: final Frame of the animation is not set")
        if self.frame_rate is None:
            raise TypeError("Error: Frame rate is not set")
        if self.ddd_layers is None or self.ddd_layers != 0 or self.ddd_layers != 1:
            raise TypeError("Error: 3d layers parameter is not set or erroneous")
        if self.width is None:
            raise TypeError("Error: Width is not set")
        if self.height is None:
            raise TypeError("Error: Height is not set")
        if self.layers is None:
            raise TypeError("Error: Animation layers not set")

    @property
    def name(self):
        if 'nm' in self.main:
            return self.main['nm']
        else:
            return None

    @name.setter
    def name(self, name : str):
        self.main['nm'] = name

    @property
    def in_point(self):
        if 'ip' in self.main:
            return self.main['ip']
        else:
            return None

    @in_point.setter
    def in_point(self, in_point : int):
        self.main['ip'] = in_point

    @property
    def out_point(self):
        if 'op' in self.main:
            return self.main['op']
        else:
            return None

    @out_point.setter
    def out_point(self, out_point : int):
        self.main['op'] = out_point

    @property
    def frame_rate(self):
        if 'fr' in self.main:
            return self.main['fr']
        else:
            return None

    @frame_rate.setter
    def frame_rate(self, frame_rate: int):
        self.main['fr'] = frame_rate

    @property
    def ddd_layers(self):
        if 'ddd' in self.main:
            return self.main['ddd']
        else:
            return None

    @ddd_layers.setter
    def ddd_layers(self, out_point: int):
        self.main['ddd'] = out_point

    @property
    def width(self):
        if 'w' in self.main:
            return self.main['w']
        else:
            return None

    @width.setter
    def width(self, width: float):
        self.main['w'] = width

    @property
    def height(self):
        if 'h' in self.main:
            return self.main['h']
        else:
            return None

    @height.setter
    def height(self, height: float):
        self.main['h'] = height

    @property
    def bodymovin_version(self):
        if 'v' in self.main:
            return self.main['v']
        else:
            return None

    @bodymovin_version.setter
    def bodymovin_version(self, bodymovin_version: str):
        self.main['v'] = bodymovin_version

    @property
    def assets(self):
        if 'assets' in self.main:
            return self.main['assets']
        else:
            return None

    @assets.setter
    def assets(self, assets: list):
        self.main['nm'] = assets

    @property
    def fonts(self):
        if 'fonts' in self.main:
            return self.main['fonts']
        else:
            return None

    @fonts.setter
    def fonts(self, fonts: list):
        self.main['fonts'] = fonts

    @property
    def chars(self):
        if 'chars' in self.main:
            return self.main['chars']
        else:
            return None

    @chars.setter
    def chars(self, lottie_chars: list):
        self.main['chars'] = lottie_chars

    @property
    def markers(self):
        if 'markers' in self.main:
            return self.main['markers']
        else:
            return None

    @markers.setter
    def markers(self, lottie_markers: list):
        self.main['markers'] = lottie_markers

    @property
    def layers(self):
        if 'layers' in self.main:
            return self.main['layers']
        else:
            return None

    @layers.setter
    def layers(self, lottie_layers: list):
        self.main['markers'] = lottie_layers