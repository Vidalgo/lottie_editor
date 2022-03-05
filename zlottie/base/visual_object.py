from zlottie.base import LottieObject, LottieAttribute
from typing import Optional


class VisualObject(LottieObject):
    name: Optional[str] = LottieAttribute(tag='nm', description='Name, as seen from editors and the like')
    match_name: Optional[str] = LottieAttribute(tag='mn', description='Match name, used in expression')
