import pydantic
from typing import Optional, Any
from lottie_search_and_replace import load_json
from lottie_animation import Lottie_animation


TRANSFORM_OPERATION_TYPES = ['translate', 'scaling', 'rotation', 'skew']
OTHER_OPERATION_TYPES = ['merge']


class Single_operation(pydantic.BaseModel):
    operation_type: str
    operation_id: int
    state: dict
    state: Optional[dict]
    operation: Any


class Multiple_operation_on_lottie_elements(pydantic.BaseModel):
    element_ids: list
    operations: list[Single_operation]


class All_lottie_Operations(pydantic.BaseModel):
    version: str
    asset_id: str
    operation_index: int
    operations: list[Multiple_operation_on_lottie_elements]


class Lottie_animation_manipulator:
    def __init__(self, lottie_animation: Lottie_animation, all_lottie_operations: dict):
        self._lottie = lottie_animation
        self._lottie_operations = All_lottie_Operations(**all_lottie_operations)

    def apply_operations_on_elements(self) -> None:
        for multiple_operation_on_lottie_elements in self._lottie_operations.operations:
            for element_id in multiple_operation_on_lottie_elements.element_ids:
                for single_operation in multiple_operation_on_lottie_elements.operations:
                    self._apply_single_operation(element_id, single_operation)

    @property
    def lottie(self):
        return self._lottie

    def _apply_single_operation(self, element_id: str, operation: Single_operation):
        lottie_element = self._lottie.vidalgo_lottie_elements[element_id]
        if operation.operation_type in TRANSFORM_OPERATION_TYPES:
            getattr(lottie_element.transform, operation.operation_type).transform = operation.operation
        elif operation.operation_type in OTHER_OPERATION_TYPES:
            lottie_merge = Lottie_animation()
            lottie_merge.load(operation.operation[0])
            lottie_element += lottie_merge
        else:
            pass


if __name__ == '__main__':
    la1 = Lottie_animation()
    la1.load("D:\\lottie_files_path\\vidalgo_vdoggie.json")
    lottie_operations = load_json("D:\\lottie_files_path\\operations_1.json")
    lottie_manipulator = Lottie_animation_manipulator(la1, lottie_operations)
    lottie_manipulator.apply_operations_on_elements()
    lottie_manipulator.lottie.name = "vdoggie_manipulated"
    lottie_manipulator.lottie.store()
