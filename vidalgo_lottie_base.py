import string
import random
import copy

from helpers import generate_random_id, update_intersected_ids
from lottie_search_and_replace import load_json, store_json


VIDALGO_ID = 'cl'
ID_SUFFIX = '_'
SYMBOLS = string.ascii_letters + string.digits + string.punctuation
PATH = "/lottie_files_path/"


class Vidalgo_lottie_base:
    def __init__(self):
        self._lottie_obj = None
        random.seed()

    def generate_random_id(self):
        self._lottie_obj[VIDALGO_ID] = ''.join(random.choice(SYMBOLS) for i in range(12))

    def load(self, animation_file_name):
        self._lottie_obj = load_json(animation_file_name)

    def copy(self, animation: dict):
        self._lottie_obj = copy.deepcopy(animation)
        self.analyze()

    def analyze(self):
        if type(self._lottie_obj) is not dict:
            raise TypeError("Error: composition is not of type dictionary")

    @property
    def lottie(self):
        return self._lottie_obj

    @lottie.setter
    def lottie(self, lottie: dict):
        self._lottie_obj = lottie
        self.analyze()
