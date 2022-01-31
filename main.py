#import lottie_transforms as lt
from lottie_animation import Lottie_animation
#from image import Image
import image
from image_layer import Image_layer
from transform import Transform
from PIL import Image

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
    la = Lottie_animation("generated_animation_1")
    la.width = 800
    la.height = 1200

    image_path = IMAGES_PATH + 'App_Icon.png'
    img1 = Image.open(image_path)
    width, height = img1.size
    img1_asset = image.Image(image_id="vidalgo icon", image_name="vidalgo icon", image_path=image_path, width=width,
                             height=height)
    img1_transform = Transform()
    img1_layer = Image_layer(layer_id=1, layer_name="Vidalgo icon layer", reference_id="vidalgo icon", in_point=1,
                             out_point=20, layer_transform=img1_transform)
    img1_transform.scaling = [20, 20, 100]
    la.add_image(img1_asset)
    la.add_main_layer(img1_layer)

    image_path = IMAGES_PATH + 'Vidalgo_Logo_BIG.jpg'
    img2 = Image.open(image_path)
    width, height = img2.size
    img2_asset = image.Image(image_id="vidalgo logo", image_name="vidalgo logo", image_path=image_path, width=width,
                             height=height)
    img2_transform = Transform()
    img2_transform.position = [600, 1000, 0]
    img2_transform.scaling = [20, 20, 100]
    img2_layer = Image_layer(layer_id=25, layer_name="Vidalgo logo layer", reference_id="vidalgo logo", in_point=10,
                             out_point=30, layer_transform=img2_transform)
    la.add_image(img2_asset)
    la.add_main_layer(img2_layer)

    image_path = IMAGES_PATH + 'women_in_red.png'
    img3 = Image.open(image_path)
    width, height = img3.size
    img3_asset = image.Image(image_id="woman in red", image_name="woman in red", image_path=image_path, width=width,
                             height=height)
    img3_transform = Transform()
    img3_layer = Image_layer(layer_id=25, layer_name="woman in red layer", reference_id="woman in red", in_point=5,
                             out_point=25, layer_transform=img3_transform)
    la.add_image(img3_asset)
    la.add_main_layer(img3_layer)

    la.store()


if __name__ == '__main__':
    '''lp = lt.Lottie_transforms('test-4.json')
    lp.parse()
    lp.transform_layer(4, delta_position=[-56, 247], delta_rotation=-47, delta_scale=[57, 63])
    lp.transform_layer(5, delta_position=[-56, 247], delta_rotation=-47, delta_scale=[57, 63])
    lp.transform_using_top_parent_null_layer(6, delta_position=[-56, 247], delta_rotation=-47, delta_scale=[57, 63])
    lp.store_lottie('test-4-transformed.json')'''
    #lottie_animation_generate()
    #lottie_animation_load()
    lottie_animation_generate_with_3_images()