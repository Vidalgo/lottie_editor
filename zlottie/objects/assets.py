from zlottie.base import LottieObject, LottieAttribute
from zlottie.objects import Composition
from typing import Optional, Any, Type, ForwardRef

Asset = ForwardRef('Asset')


class Asset(LottieObject):
    id: str = LottieAttribute(tag='id', description='Identifier used by layers when referencing this asset')

    @classmethod
    def get_load_class(cls, raw: Any) -> Type[Asset]:
        if 'e' in raw:
            return Image
        elif 'layers' in raw:
            return Precomposition
        else:
            return Sound


class Image(Asset):
    width: Optional[float] = LottieAttribute(tag='w', default=0, description='Width of the image')
    height: Optional[float] = LottieAttribute(tag='h', default=0, description='Height of the image')
    path: Optional[str] = LottieAttribute(tag='u', description='Path to the directory containing an image')
    url: str = LottieAttribute(tag='p', description='Image filename or data url')
    embedded: Optional[int] = LottieAttribute(tag='e', default=0, description='Whether the image is embedded')


class Sound(Asset):
    path: Optional[str] = LottieAttribute(tag='u', description='Path to the directory containing a sound file')
    url: str = LottieAttribute(tag='p', description='Sound filename or data url')
    embedded: Optional[int] = LottieAttribute(tag='e', default=0, description='Whether the sound is embedded')


class Precomposition(Asset, Composition):
    name: Optional[str] = LottieAttribute(tag='nm', description='Name of the precomposition')
    framerate: Optional[float] = LottieAttribute(tag='fr', description='Framerate in frames per second')


__all__ =['Asset', 'Image', 'Sound', 'Precomposition']
