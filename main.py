# import lottie_transforms as lt
from lottie_animation import Lottie_animation
# from image import Image
from image_asset import Image_asset
from image_layer import Image_layer
from transform import Transform
from font import Font
from text_layer import Text_layer
from text_animator_data import Text_animator_data
from PIL import Image

LOTTIE_PATH = "\\lottie_files_path\\"
IMAGES_PATH = "\\lottie_files_path\\images\\"


def lottie_animation_generate():
    la = Lottie_animation()
    la.create("generated_animation_1")
    la.store()


def lottie_animation_1_load():
    la = Lottie_animation()
    la.load("D:\\lottie_files_path\\48713-media-people.json")
    la.name = "test_1"
    la.store()
    pass


def lottie_animation_2_load():
    la = Lottie_animation()
    la.load("D:\\lottie_files_path\\Happy Purim decorations.json")
    la.name = "test_2"
    la.store()
    pass


def lottie_animation_3_load():
    la = Lottie_animation()
    la.load("D:\\lottie_files_path\\Snow_Boarding.json")
    la.name = "test_3"
    la.store()
    pass


def combine_animations_1():
    la1 = Lottie_animation()
    la1.load("D:\\lottie_files_path\\vdoggie.json")
    la2 = Lottie_animation()
    la2.load("D:\\lottie_files_path\\fairy.json")
    la1 += la2
    la1.name = "vdoggie_plus_fairy"
    la1.store()

def combine_animations_2():
    la1 = Lottie_animation()
    la1.load("D:\\lottie_files_path\\coin.json")
    la2 = Lottie_animation()
    la2.load("D:\\lottie_files_path\\coin.json")
    la3 = Lottie_animation()
    la3.load("D:\\lottie_files_path\\coin.json")
    for count in range(100):
        la1 += la2
    la1.name = "coin_plus_coin"
    la1.store()

def combine_animations_3():
    la1 = Lottie_animation()
    la1.load("D:\\lottie_files_path\\vdoggie.json")
    la2 = Lottie_animation()
    la2.load("D:\\lottie_files_path\\vdoggie.json")
    la1 += la2
    la1 += la2
    la1 += la2
    la1.name = "vdoggie_plus_vdoggie"
    la1.store()

def combine_animations_4():
    la1 = Lottie_animation()
    la1.load("D:\\lottie_files_path\\fairy.json")
    la2 = Lottie_animation()
    la2.load("D:\\lottie_files_path\\fairy.json")
    la1 += la2
    la1 += la2
    la1 += la2
    la1.name = "fairy_plus_fairy"
    la1.store()

def lottie_animation_generate_with_3_images():
    la = Lottie_animation(lottie_name="generated_animation_1", width=800, height=1200)

    image_path = IMAGES_PATH + 'App_Icon.png'
    img1_asset = Image_asset(image_id="vidalgo icon", image_path=image_path)
    img1_transform = Transform()
    img1_layer = Image_layer(layer_id=1, layer_name="Vidalgo icon layer", reference_id="vidalgo icon", in_point=1,
                             out_point=20, layer_transform=img1_transform)
    img1_transform.scaling = [20, 20, 100]
    la.add_image(img1_asset)
    la.add_main_layer(img1_layer)

    image_path = IMAGES_PATH + 'Vidalgo_Logo_BIG.jpg'
    img2_asset = Image_asset(image_id="vidalgo logo", image_path=image_path)
    img2_transform = Transform()
    img2_transform.position = [600, 1000, 0]
    img2_transform.scaling = [20, 20, 100]
    img2_layer = Image_layer(layer_id=25, layer_name="Vidalgo logo layer", reference_id="vidalgo logo", in_point=10,
                             out_point=30, layer_transform=img2_transform)
    la.add_image(img2_asset)
    la.add_main_layer(img2_layer)

    image_path = IMAGES_PATH + 'women_in_red.png'
    img3_asset = Image_asset(image_id="woman in red", image_path=image_path)
    img3_transform = Transform()
    img3_layer = Image_layer(layer_id=25, layer_name="woman in red layer", reference_id="woman in red", in_point=5,
                             out_point=25, layer_transform=img3_transform)
    la.add_image(img3_asset)
    la.add_main_layer(img3_layer)

    la.store()


def lottie_animation_generate_with_1_image():
    la = Lottie_animation(lottie_name="static_image_animation_1", width=400, height=400, in_point=1, out_point=30)
    image_path = IMAGES_PATH + 'App_Icon.png'
    img1_asset = Image_asset(image_id="vidalgo icon", image_path=image_path)
    img1_transform = Transform()
    img1_layer = Image_layer(layer_id=1, layer_name="Vidalgo icon layer", reference_id="vidalgo icon", in_point=1,
                             out_point=30, layer_transform=img1_transform)
    img1_transform.scaling = [100, 100, 100]
    la.add_image(img1_asset)
    la.add_main_layer(img1_layer)
    la.store()


def lottie_animation_load_replace_delete():
    la = Lottie_animation()
    la.load(LOTTIE_PATH + 'generated_animation_1.json')
    image_path = IMAGES_PATH + 'elegant_woman.png'
    img1_asset = Image_asset(image_id="elegant woman", image_path=image_path)
    la.replace_image(img1_asset, 'woman in red')
    la.name = 'generated_animation_2'
    im1_layer = la.find_main_layer(2)
    im1_layer.name = "elegant woman layer"
    im1_layer.reference_id = "elegant woman"
    im1_layer.transform.scaling = [50, 50, 0]

    la.delete_main_layer(1)
    la.delete_image('vidalgo logo')
    la.store()


def lottie_animation_generate_with_1_text():
    la = Lottie_animation(lottie_name="static_text_animation_1", width=500, height=500, in_point=1, out_point=30)
    default_font = Font()
    la.add_font(default_font)
    text1_layer = Text_layer(layer_id=1, layer_name="text layer", in_point=1, out_point=30)
    text1_layer.transform.position = [100, 250, 0]
    la.add_main_layer(text1_layer)
    la.store()


def load_animation_and_add_another_one_1():
    la1 = Lottie_animation()
    la1.load(LOTTIE_PATH + "Lower-Third-instagram.json")
    la1.name = "instagram_and_people"
    la2 = Lottie_animation()
    la2.load(LOTTIE_PATH + "48713-media-people.json")
    la3 = Lottie_animation()
    la3.load(LOTTIE_PATH + "48713-media-people.json")
    la4 = Lottie_animation()
    la4.load(LOTTIE_PATH + "48713-media-people.json")
    la1 += la2
    la1 += la3
    la1 += la4
    la1.store()


def merge_layer_and_image_animations():
    la1 = Lottie_animation()
    la1.load(LOTTIE_PATH + "static_image_animation_1.json")
    la1.name = "static_image_and_text"
    la2 = Lottie_animation()
    la2.load(LOTTIE_PATH + "static_text_animation_1.json")
    la1 += la2
    la1.find_main_layer(1).transform.position = [100, 700, 0]
    la1.store()


def add_image_to_lower_thirds():
    la = Lottie_animation()
    la.load(LOTTIE_PATH + "Lower-Third-instagram.json")
    la.name = "instagram_with_image"
    icon_place_holder_layer = la.find_main_layer(4)
    icon_place_holder_layer.hide()
    icon_place_holder_transform = Transform()
    icon_place_holder_transform.copy(icon_place_holder_layer.transform)
    icon_place_holder_transform.anchor = [50, 50, 0]
    image_path = IMAGES_PATH + 'Instagram-logo-transparent-PNG.png'
    img_asset = Image_asset(image_id="instagram icon", image_path=image_path, width=100, height=100)
    img_layer = Image_layer(layer_id=1000, layer_name="instagram icon layer", reference_id="instagram icon", in_point=5,
                            out_point=175, layer_transform=icon_place_holder_transform)
    la.add_image(img_asset)
    la.add_main_layer(img_layer, update_layer_id=False, order="after", layer_id=4)
    la.store()


def transfer_image_and_text():
    la = Lottie_animation()
    la.load(LOTTIE_PATH + "instagram_with_image.json")
    la.name = "vidalgo_lower_third"
    image_path = IMAGES_PATH + 'App_Icon.png'
    img_asset = Image_asset(image_id="App_Icon icon", image_path=image_path, width=100, height=100)
    la.replace_image(img_asset, "instagram icon")
    text_layer = la.find_main_layer(2)
    text_layer.text = "hello world"
    la.store()


class Parent:
    def __init__(self):
        self._parent = {}

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent: dict):
        self._parent = parent


class Child_1(Parent):
    def __init__(self):
        super().__init__()

    @property
    def child_1(self):
        return Parent.parent

    @child_1.setter
    def child_1(self, child_1: dict):
        Parent.parent = child_1


class Child_2(Parent):
    def __init__(self):
        Parent.__init__(self)

    @property
    def child_2(self):
        return Parent.parent

    @child_2.setter
    def child_2(self, child_2: dict):
        Parent.parent = child_2


if __name__ == '__main__':
    '''p = Parent()
    p.parent = {'pa': 1, 'pb': 2}
    c1 = Child_1()
    c1.child_1 = {'c1a': 1, 'c1b': 2}
    c2 = Child_2()
    c2.child_2 = {'c2a': 1, 'c2b': 2}
    print(p.parent)
    print(c1.child_1)
    print(c2.child_2)'''

    '''lp = lt.Lottie_transforms('test-4.json')
    lp.parse()
    lp.transform_layer(4, delta_position=[-56, 247], delta_rotation=-47, delta_scale=[57, 63])
    lp.transform_layer(5, delta_position=[-56, 247], delta_rotation=-47, delta_scale=[57, 63])
    lp.transform_using_top_parent_null_layer(6, delta_position=[-56, 247], delta_rotation=-47, delta_scale=[57, 63])
    lp.store_lottie('test-4-transformed.json')'''
    # lottie_animation_1_load()
    # lottie_animation_2_load()
    # lottie_animation_3_load()
    #combine_animations_1()
    #combine_animations_2()
    #combine_animations_3()
    combine_animations_4()
    # lottie_animation_generate()
    # ottie_animation_generate_with_3_images()
    # lottie_animation_load_replace_delete()
    # lottie_animation_text_layer_create()
    # load_animation_and_add_another_one()
    # lottie_animation_generate_with_1_image()
    # lottie_animation_generate_with_1_text()
    # merge_layer_and_image_animations()
    # add_image_to_lower_thirds()
    # transfer_image_and_text()
