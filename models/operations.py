from pydantic import BaseModel, Field, confloat, conlist
from enum import Enum
from typing import Literal, Union, Any

# aliases
Lottie = dict


# generics
class OperationType(str, Enum):
    # transform operations
    Position = 'position'
    Scaling = 'scaling'
    Rotation = 'rotation'
    Skew = 'skew'
    # other
    Merge = 'merge'


class OperationBase(BaseModel):
    type: OperationType = Field(..., description='operation type')


# transforms
class TransformOperation(OperationBase):
    element_id: str = Field(..., description='target element id')
    value: Any = Field(None, description='operation value')


class PositionTransformOperation(TransformOperation):
    type: Literal[OperationType.Position]
    value: conlist(float, min_items=2, max_items=2) = Field(..., description='new (x,y) values')


class RotationTransformOperation(TransformOperation):
    type: Literal[OperationType.Rotation]
    value: confloat(ge=0, lt=360) = Field(..., description='counter-clockwise rotation degrees')


# merges
class MergeOperation(OperationBase):
    type: Literal[OperationType.Merge]
    animations: list[Lottie] = Field(..., description='list of lotties to merge')


# all operations
LottieOperation = Union[
    RotationTransformOperation,
    PositionTransformOperation,
    MergeOperation
]

if __name__ == '__main__':
    import json
    from pydantic import parse_raw_as

    # encode
    operations = [
        {'type': OperationType.Rotation, 'element_id': '111', 'value': 15.0},
        {'type': OperationType.Position, 'element_id': '222', 'value': [10.0, 20.0]},
        {'type': OperationType.Merge, 'animations': [{'a': 1}, {'b': 2}]}
    ]
    encoded = json.dumps(operations)

    # decode
    parsed = parse_raw_as(list[LottieOperation], encoded)

    # assert
    expected = [
        RotationTransformOperation(type=OperationType.Rotation, element_id='111', value=15.0),
        PositionTransformOperation(type=OperationType.Position, element_id='222', value=[10.0, 20.0]),
        MergeOperation(type=OperationType.Merge, animations=[{'a': 1}, {'b': 2}])
    ]
    assert not any(a != b for a, b in zip(parsed, expected)), '*** Parse failed! ***'
