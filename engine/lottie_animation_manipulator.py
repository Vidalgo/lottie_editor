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
            current_value = getattr(lottie_element.transform, operation.type)
            if operation.type == OperationType.Position:
                new_value = [c + n for c, n in zip(current_value['k'], operation.value)]
            elif operation.type == OperationType.Rotation:
                new_value = current_value['k'] + operation.value
            elif operation.type == OperationType.Scaling:
                new_value = [c * n/100.0 for c, n in zip(current_value['k'], operation.value)]
            setattr(lottie_element.transform, operation.type, new_value)
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
    '''la1 = Lottie_animation()
    la1.load("D:\\lottie_files_path\\60875-confuse-person.json")
    la1.name = "zlottie_60875-confuse-person"
    la1.add_lottie_id()
    la1.store()'''

    lottie_operations = [
        PositionTransformOperation(element_id='zlQxBpiOiYPVet', value=[0, 0]),
        ScalingTransformOperation(element_id='zlQxBpiOiYPVet', value=[25, 125]),
        RotationTransformOperation(element_id='zlQxBpiOiYPVet', value=45),
        #MergeOperation(animations=[la2.lottie])
    ]

    la = Lottie_animation()
    la.load("D:\\lottie_files_path\\zlottie_60875-confuse-person.json")
    lottie_manipulator = Lottie_animation_manipulator(la, lottie_operations)
    lottie_manipulator.apply_operations_on_elements()
    lottie_manipulator.lottie.name = "zlottie_60875-confuse-person"
    lottie_manipulator.lottie.store()
