#import lottie_transforms as lt
from lottie_animation import Lottie_animation
#from image import Image
from image_asset import Image_asset
from image_layer import Image_layer
from transform import Transform
from font import Font
from text_layer import Text_layer
from text_data import Text_data
from PIL import Image

LOTTIE_PATH = "\\lottie_files_path\\"
IMAGES_PATH = "\\lottie_files_path\\images\\"


def lottie_animation_generate():
    la = Lottie_animation()
    la.create("generated_animation_1")
    la.store()


def lottie_animation_load():
    la = Lottie_animation()
    la.load("D:\\lottie_files_path\\coin.json")
    pass


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


def lottie_animation_text_layer_create():
    la = Lottie_animation(lottie_name="generated_animation_3", width=500, height=500)
    font = Font()
    la.add_font(font)
    text1_layer = Text_layer(layer_id=1, layer_name="text layer", in_point=0, out_point=30)
    text1_layer.transform.position = [100, 250, 0]
    la.add_main_layer(text1_layer)
    la.store()

def load_animation_and_add_another_one():
    la1 = Lottie_animation()
    la1.load(LOTTIE_PATH + "Lower-Third-instagram.json")
    la1.name = "instagram_and_people"
    la2 = Lottie_animation()
    la2.load(LOTTIE_PATH + "48713-media-people.json")
    la1 += la2
    la1.store()
    pass




if __name__ == '__main__':
    '''lp = lt.Lottie_transforms('test-4.json')
    lp.parse()
    lp.transform_layer(4, delta_position=[-56, 247], delta_rotation=-47, delta_scale=[57, 63])
    lp.transform_layer(5, delta_position=[-56, 247], delta_rotation=-47, delta_scale=[57, 63])
    lp.transform_using_top_parent_null_layer(6, delta_position=[-56, 247], delta_rotation=-47, delta_scale=[57, 63])
    lp.store_lottie('test-4-transformed.json')'''
    #lottie_animation_generate()
    #lottie_animation_load()
    #ottie_animation_generate_with_3_images()
    #lottie_animation_load_replace_delete()
    #lottie_animation_text_layer_create()
    load_animation_and_add_another_one()