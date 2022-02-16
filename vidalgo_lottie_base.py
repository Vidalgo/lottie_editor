import string
import random
import copy

from lottie_search_and_replace import load_json, store_json


VIDALGO_ID = 'ln'
ID_SUFFIX = '_'
SYMBOLS = string.ascii_letters + string.digits + string.punctuation
PATH = "/lottie_files_path/"

class Vidalgo_lottie_base:
    _RANDOM_SEED_CALLED = False

    def __init__(self):
        self._lottie_obj = {}
        if not Vidalgo_lottie_base._RANDOM_SEED_CALLED:
            random.seed()
            Vidalgo_lottie_base._RANDOM_SEED_CALLED = True

    @staticmethod
    def uuid(length: int = 12):
        return ''.join(random.choice(SYMBOLS) for i in range(length))

    def generate_random_id(self, length: int = 12):
        self._lottie_obj[VIDALGO_ID] = self.uuid()

    def load(self, animation_file_name):
        self._lottie_obj = load_json(animation_file_name)
        self.generate_random_id()

    def copy(self, animation: dict):
        self._lottie_obj = copy.deepcopy(animation)
        self.analyze()

    def analyze(self):
        if type(self._lottie_obj) is not dict:
            raise TypeError("Error: composition is not of type dictionary")
        if self.vidalgo_id is None:
            raise TypeError("Error: layer doesn't have a vidalgo id")

    @property
    def lottie_base(self):
        return self._lottie_obj

    @lottie_base.setter
    def lottie_base(self, lottie: dict):
        self._lottie_obj = lottie
        if lottie is not None and VIDALGO_ID not in lottie:
            self.generate_random_id()
        self.analyze()

    @property
    def vidalgo_id(self):
        if VIDALGO_ID in self._lottie_obj:
            return self._lottie_obj[VIDALGO_ID]
        else:
            return None

    @vidalgo_id.setter
    def vidalgo_id(self, vidalgo_id):
        self._lottie_obj[VIDALGO_ID] = vidalgo_id

    @property
    def lottie_element_id(self):
        if 'ind' in self.lottie_base:
            return self.lottie_base['ind']
        elif 'id' in self.lottie_base:
            return self.lottie_base['id']
        elif 'fName' in self.lottie_base:
            return self.lottie_base['fName']
        elif 'fFamily' in self.lottie_base:
            return self.lottie_base['fFamily']
        else:
            return None

    @lottie_element_id.setter
    def lottie_element_id(self, lottie_element_id):
        if 'ind' in self.lottie_base and type(lottie_element_id) is int:
            self.lottie_base['ind'] = lottie_element_id
        elif 'id' in self.lottie_base:
            self.lottie_base['id'] = lottie_element_id
        elif 'fName' in self.lottie_base:
            self.lottie_base['fName'] = lottie_element_id
        elif 'fFamily' in self.lottie_base:
            self.lottie_base['fFamily'] = lottie_element_id
