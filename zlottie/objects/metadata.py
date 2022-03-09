from zlottie.base import LottieObject, LottieAttribute
from typing import Optional, List


class Metadata(LottieObject):
    author: Optional[str] = LottieAttribute(tag='a', description='Author')
    keywords: Optional[List[str]] = LottieAttribute(tag='k', description='Keywords')
    description: Optional[str] = LottieAttribute(tag='d', description='Description')
    theme_color: Optional[str] = LottieAttribute(tag='tc', description='Theme Color')
    generator: Optional[str] = LottieAttribute(tag='g', description='Software used to generate the file')


if __name__ == '__main__':
    m = Metadata()
    print('asd')
