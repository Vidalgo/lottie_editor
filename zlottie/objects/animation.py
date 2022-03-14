from zlottie.base import LottieAttribute
from zlottie.objects import Composition, VisualObject, Metadata, RawObject, Asset
from typing import Optional, List


class Animation(VisualObject, Composition):
    # TODO: replace RawObject with actual lottie objects
    version: Optional[str] = LottieAttribute(tag='v', description='version x.y.z')
    frame_rate: float = LottieAttribute(tag='fr', description='Framerate in frames per second')
    in_point: float = LottieAttribute(tag='ip', description='"In Point", which frame the animation starts at (usually 0)')
    out_point: float = LottieAttribute(tag='op', description='"Out Point", which frame the animation stops/loops at, which makes this the duration in frames when `ip` is 0')
    width: int = LottieAttribute(tag='w', description='Width of the animation')
    height: int = LottieAttribute(tag='h', description='Height of the animation')
    three_dimensional: Optional[int] = LottieAttribute(tag='ddd', default=0, description='Is animation 3D (always 0)')
    assets: Optional[List[Asset]] = LottieAttribute(tag='assets', description='List of assets')
    fonts: Optional[List[RawObject]] = LottieAttribute(tag='fonts', description='Fonts')
    chars: Optional[List[RawObject]] = LottieAttribute(tag='chars', description='Data defining text characters as lottie shapes')
    metadata: Optional[Metadata] = LottieAttribute(tag='meta', description='Document metadata')
    markers: Optional[List[RawObject]] = LottieAttribute(tag='markers', description='Markers defining named sections of the composition')
    motion_blur: Optional[RawObject] = LottieAttribute(tag='mb', description='Motion blur')

    def __repr__(self):
        return f"<Animation ('{self.name}')>"
