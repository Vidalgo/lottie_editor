import string
import random
import copy
from pathlib import Path
from typing import Union

from engine.lottie_search_and_replace import load_json, store_json

VIDALGO_ID = 'ln'
ZLOTTIE_OBJECT_ID = 'zlottie'
ID_SUFFIX = '_'
SYMBOLS = (string.ascii_letters + string.digits)

PROJECT_ROOT = Path(__file__).parents[1]
PATH = PROJECT_ROOT.joinpath('output')


class Vidalgo_lottie_base:
    _RANDOM_SEED_CALLED = False
    vidalgo_lottie_elements: dict = {}

    def __init__(self):
        self._lottie_obj = {}
        if not Vidalgo_lottie_base._RANDOM_SEED_CALLED:
            random.seed()
            Vidalgo_lottie_base._RANDOM_SEED_CALLED = True
        self.generate_random_id()

    def refactor_id(self):
        self.lottie_element_id = self.lottie_element_id if type(self.lottie_element_id) is str \
            else self.lottie_element_id
        return self.lottie_element_id

    @staticmethod
    def uuid(length: int = 12):
        return 'zl' + ''.join(random.choice(SYMBOLS) for i in range(length))

    def generate_random_id(self, length: int = 12):
        self._lottie_obj[VIDALGO_ID] = self.uuid(length)

    def load(self, animation_file_name):
        if isinstance(animation_file_name, str):
            self._lottie_obj = load_json(animation_file_name)
        else:
            self._lottie_obj = animation_file_name
        if self._lottie_obj is not None and VIDALGO_ID not in self._lottie_obj:
            self.generate_random_id()
        Vidalgo_lottie_base.vidalgo_lottie_elements[self.vidalgo_id] = self

    def copy(self, animation: dict):
        self._lottie_obj = copy.deepcopy(animation)
        self.analyze()

    def analyze(self):
        if type(self._lottie_obj) is not dict:
            raise TypeError("Error: composition is not of type dictionary")
        if self.vidalgo_id is None:
            raise TypeError("Error: layer doesn't have a vidalgo id")

    def add_lottie_id(self):
        Vidalgo_lottie_base._add_ids_to_elements(self._lottie_obj)

    @property
    def lottie_base(self):
        return self._lottie_obj

    @lottie_base.setter
    def lottie_base(self, lottie: dict):
        self._lottie_obj = lottie
        if lottie is not None and VIDALGO_ID not in lottie:
            self.generate_random_id()
        Vidalgo_lottie_base.vidalgo_lottie_elements[self.vidalgo_id] = self
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
    def zlottie_id(self):
        if 'cl' in self._lottie_obj:
            return self._lottie_obj['cl']
        else:
            return None

    def set_zlottie_id(self):
        self._lottie_obj['cl'] = ZLOTTIE_OBJECT_ID

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
        elif 'nm' in self.lottie_base:
            return self.lottie_base['nm']
        else:
            return None

    @lottie_element_id.setter
    def lottie_element_id(self, lottie_element_id):
        lottie_element_uuid = '{0}_{1}'.format(lottie_element_id, self.uuid(4))
        if 'ind' in self.lottie_base and type(lottie_element_id) is int:
            self.lottie_base['ind'] = lottie_element_id
        elif 'id' in self.lottie_base:
            self.lottie_base['id'] = lottie_element_uuid
        elif 'fName' in self.lottie_base:
            self.lottie_base['fName'] = lottie_element_uuid
        elif 'fFamily' in self.lottie_base:
            self.lottie_base['fFamily'] = lottie_element_uuid

    @staticmethod
    def remove_uuid(lottie_element_uuid: str):
        return lottie_element_uuid.rsplit('_', 1)[0] if lottie_element_uuid is not None else None

    @staticmethod
    def _add_ids_to_elements(lottie_obj: dict):
        if VIDALGO_ID not in lottie_obj:
            lottie_obj[VIDALGO_ID] = Vidalgo_lottie_base.uuid()
        for key in lottie_obj:
            if type(lottie_obj[key]) is dict:
                Vidalgo_lottie_base._add_ids_to_elements(lottie_obj[key])
            elif type(lottie_obj[key]) is list:
                [Vidalgo_lottie_base._add_ids_to_elements(element) for element in lottie_obj[key]
                 if type(element) is dict]


