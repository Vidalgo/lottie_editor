from zlottie.base import LottieObject, LottieAttribute
from typing import List


class Composition(LottieObject):
    # TODO: annotate with actual schema
    layers: List[LottieObject] = LottieAttribute(tag='layers', description='composition layers')

# actual schema is:
# layers: List[Union[
#         PrecompositionLayer,
#         SolidColorLayer,
#         ImageLayer,
#         NullLayer,
#         ShapeLayer,
#         TextLayer,
#         AudioLayer,
#     ]]
