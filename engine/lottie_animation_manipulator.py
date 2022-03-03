import pydantic
from typing import Optional, Any
from engine.lottie_search_and_replace import load_json
from engine.lottie_animation import Lottie_animation
from models import *

# TRANSFORM_OPERATION_TYPES = ['position', 'scaling', 'rotation', 'skew']
# OTHER_OPERATION_TYPES = ['merge']
#
#
# class Single_operation(pydantic.BaseModel):
#     operation_type: str
#     operation_id: int
#     state: Optional[dict]
#     operation: Any
#
#
# class Multiple_operation_on_lottie_elements(pydantic.BaseModel):
#     element_ids: list
#     operations: list[Single_operation]
#
#
# class All_lottie_Operations(pydantic.BaseModel):
#     version: str
#     asset_id: str
#     operation_index: int
#     operations: list[Multiple_operation_on_lottie_elements]


class Lottie_animation_manipulator:
    def __init__(self, lottie_animation: Lottie_animation, all_lottie_operations: list[LottieOperation]):
        self._lottie = lottie_animation
        self._lottie_operations = all_lottie_operations

    def apply_operations_on_elements(self) -> None:
        for operation in self._lottie_operations:
            self._apply_single_operation(operation)

    @property
    def lottie(self):
        return self._lottie

    def _apply_single_operation(self, operation: LottieOperation):
        if isinstance(operation, TransformOperation):
            lottie_element = self._lottie.vidalgo_lottie_elements[operation.element_id]
            setattr(lottie_element.transform, operation.type, operation.value)
        elif isinstance(operation, MergeOperation):
            element_id = self._lottie.lottie['ln']
            lottie_element = self._lottie.vidalgo_lottie_elements[element_id]
            for animation in operation.animations:
                lottie_merge = Lottie_animation()
                lottie_merge.load(animation)
                lottie_element += lottie_merge
        else:
            pass


if __name__ == '__main__':
    la1 = Lottie_animation()
    la1.load("D:\\lottie_files_path\\vidalgo_vdoggie.json")
    la2 = Lottie_animation()
    la2.load("D:\\lottie_files_path\\coin.json")

    lottie_operations = [
        ScalingTransformOperation(element_id='$6fy{Q{{=Noh', value=[50,80]),
        RotationTransformOperation(element_id='$6fy{Q{{=Noh', value=45),
        MergeOperation(animations=[la2.lottie])
    ]

    lottie_manipulator = Lottie_animation_manipulator(la1, lottie_operations)
    lottie_manipulator.apply_operations_on_elements()
    lottie_manipulator.lottie.name = "vdoggie_manipulated"
    lottie_manipulator.lottie.store()
