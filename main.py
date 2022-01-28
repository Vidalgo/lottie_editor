from lottie.utils import script
from lottie_animation import Lottie_animation

import lottie_to_frame
import lottie_transforms as lt
from lottie_animation import Lottie_animation

def lottie_animation_generate():
    la = Lottie_animation()
    la.create("generated_animation_1")
    la.store()

def lottie_animation_generate_load():
    pass


def to_frame():
    my_file = 'Birthday-Card'
    lottie_file = f'{my_file}.json'
    frame_number = 0

    jpg_output_file_quality = 25

    lft = lottie_to_frame.LottieToImage(lottie_file)
    for counter in range(21):
        frame_number = counter * 10
        svg_output_file = f'.\\temp\\{my_file}{frame_number}.svg'
        png_output_file = f'.\\temp\\{my_file}{frame_number}.png'
        jpg_output_file = f'.\\temp\\{my_file}{frame_number}.jpg'
        lft.to_svg(svg_output_file, frame_number=frame_number)
        lft.to_png(png_output_file, frame_number=frame_number)
        lft.to_jpg(jpg_output_file, frame_number=frame_number, quality=jpg_output_file_quality)


if __name__ == '__main__':
    '''lp = lt.Lottie_transforms('test-4.json')
    lp.parse()
    lp.transform_layer(4, delta_position=[-56, 247], delta_rotation=-47, delta_scale=[57, 63])
    lp.transform_layer(5, delta_position=[-56, 247], delta_rotation=-47, delta_scale=[57, 63])
    lp.transform_using_top_parent_null_layer(6, delta_position=[-56, 247], delta_rotation=-47, delta_scale=[57, 63])
    lp.store_lottie('test-4-transformed.json')'''
    lottie_animation_generate()





