import unittest
from pathlib import Path

from engine.lottie_animation import Lottie_animation
from engine.lottie_creator import Lottie_creator

PATH = Path(__file__).parents[1].joinpath('tests')
INPUT_PATH = PATH.joinpath('inputs')
OUTPUT_PATH = PATH.joinpath('outputs')


class Test_lottie_creator(unittest.TestCase):
    @staticmethod
    def _create_zlottie(name: str) -> None:
        lottie_animation = Lottie_animation()
        input_file_name = str(INPUT_PATH.joinpath(f'{name}.json'))
        lottie_animation.load(input_file_name)
        lottie_animation.name = f'zlottie_{name}'
        output_file_name = str(INPUT_PATH.joinpath(f'{lottie_animation.name}.json'))
        lottie_animation.store(output_file_name)

    @staticmethod
    def _load_zlottie(name: str) -> Lottie_animation:
        lottie_animation = Lottie_animation()
        input_file_name = str(INPUT_PATH.joinpath(f'zlottie_{name}.json'))
        lottie_animation.load(input_file_name)
        return lottie_animation

    @staticmethod
    def _load_and_create_same_file(name: str, ids: list[str]) -> Lottie_creator:
        # Test_lottie_creator._create_zlottie(name)
        zlottie = Test_lottie_creator._load_zlottie(name)
        lc = Lottie_creator(zlottie, ids)
        lc.create("zlottie_{0}_clone".format(name))
        return lc

    @staticmethod
    def _load_and_hide_layers_same_file(name: str, ids: list[str]) -> Lottie_creator:
        # Test_lottie_creator._create_zlottie(name)
        zlottie = Test_lottie_creator._load_zlottie(name)
        lc = Lottie_creator(zlottie, ids)
        lc.hide("zlottie_{0}_clone".format(name))
        return lc

    def test_create_coin_from_coin(self):
        name = "39871-knife"
        Test_lottie_creator._create_zlottie(name)
        #lc = Test_lottie_creator._load_and_create_same_file(name, ['zlbUh5UTuZBVT7'])

    def test_people_with_mobile_phones(self):
        name = "84679-people-waiting-in-line-blue"
        lc = Test_lottie_creator._load_and_create_same_file(name, ['zlWyAPtsxiyYyk'])
        self.assertEqual(lc.original_lottie.lottie_base, lc.derived_lottie.lottie_base)  # add assertion here

    def test_complex_zlottie(self):
        name = "coin"
        lc = Test_lottie_creator._load_and_create_same_file(name, ['zlbUh5UTuZBVT7', 'zlVbzYFKVtVlKS'])
        self.assertEqual(lc.original_lottie.lottie_base, lc.derived_lottie.lottie_base)  # add assertion here

    def test_create_zlottie(self):
        name = "84679-people-waiting-in-line-blue"
        Test_lottie_creator._create_zlottie(name)
        #lc = Test_lottie_creator._load_and_create_same_file(name, ['zlRbJd5zEYsFyX'])

    def test_create_zlottie_class(self):
        name = "84679-people-waiting-in-line-blue"
        fname = str(INPUT_PATH.joinpath(f'zlottie_{name}.json'))
        la = Lottie_animation()
        la.load(fname)
        la.set_zlottie_layers(all=True)
        la.name = 'zlottie_' + name + '_view_class'
        output_file_name = str(OUTPUT_PATH.joinpath(f'{la.name}.json'))
        la.store(output_file_name)

    def test_mark_elements(self):
        name = "84679-people-waiting-in-line-blue"
        zlottie = Test_lottie_creator._load_zlottie(name)
        name += "_hide"
        lc = Lottie_creator(zlottie, ['zl3gSO31qLCeaE', 'zlfFmSJKvzOxf6'])
        lc.mark_elements(name, opacity=25, recolor=[139, 0, 0, 1])

    def test_recalc_animation_size(self):
        name = "zlottie_complex"
        Test_lottie_creator._create_zlottie(name)
        fname = str(INPUT_PATH.joinpath(f'zlottie_{name}.json'))
        la = Lottie_animation()
        la.load(fname)
        la.recalc_animation_size()
        la.name = 'zlottie_' + name + '_recalc_size'
        output_file_name = str(OUTPUT_PATH.joinpath(f'{la.name}.json'))
        la.store(output_file_name)

    def test_add_zloties_to_one_composition(self):
        name = "zlottie_coin.json"
        name = str(INPUT_PATH.joinpath(f'{name}'))
        la1 = Lottie_animation()
        la1.load(name)
        name = "zlottie_49031-guitar-music.json"
        name = str(INPUT_PATH.joinpath(f'{name}'))
        la2 = Lottie_animation()
        la2.load(name)
        name = "zlottie_39871-knife.json"
        name = str(INPUT_PATH.joinpath(f'{name}'))
        la3 = Lottie_animation()
        la3.load(name)
        name = "zlottie_19680-bell-ringing.json"
        name = str(INPUT_PATH.joinpath(f'{name}'))
        la4 = Lottie_animation()
        la4.load(name)
        la1 += la2
        la1 += la3
        la1 += la4
        la1.name = "zlottie_complex"
        output_file_name = str(OUTPUT_PATH.joinpath(f'{la1.name}.json'))
        la1.store(output_file_name)

    def test_hide_redundant_layers_lottie_1(self):
        name = "74839-car-isometric-3d-animation-navigation-car-red-car-in-nature-car-on-the-road"
        #Test_lottie_creator._create_zlottie(name)
        lc = Test_lottie_creator._load_and_hide_layers_same_file(name, ['zlRlMWmOaMAe8F'])

    def test_create_redundant_layers_lottie_1(self):
        name = "74839-car-isometric-3d-animation-navigation-car-red-car-in-nature-car-on-the-road"
        #Test_lottie_creator._create_zlottie(name)
        lc = Test_lottie_creator._load_and_create_same_file(name, ['zlJeHDUB7DZFDS', 'zlW2FLzJ65wo5e'])


if __name__ == '__main__':
    unittest.main()
