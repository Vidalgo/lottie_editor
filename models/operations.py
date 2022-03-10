from pydantic import BaseModel, Field, confloat, conint, conlist
from enum import Enum
from typing import Literal, Union, Any, Optional

# aliases
Lottie = dict


# generics
class OperationType(str, Enum):
    # transform operations
    Position = 'position'
    Scaling = 'scaling'
    Rotation = 'rotation'
    Skew = 'skew'
    Opacity = 'opacity'
    # other
    Merge = 'merge'


class OperationBase(BaseModel):
    type: OperationType = Field(..., description='operation type')


# transforms
class TransformOperation(OperationBase):
    element_id: str = Field(..., description='target element id')
    value: Any = Field(None, description='operation value')


class PositionTransformOperation(TransformOperation):
    type: Literal[OperationType.Position] = OperationType.Position
    value: conlist(int, min_items=2, max_items=2) = Field(..., description='new (x,y) values')


class RotationTransformOperation(TransformOperation):
    type: Literal[OperationType.Rotation] = OperationType.Rotation
    value: confloat(ge=0, lt=360) = Field(..., description='clockwise rotation degrees')


class ScalingTransformOperation(TransformOperation):
    type: Literal[OperationType.Scaling] = OperationType.Scaling
    value: conlist(conint(ge=0), min_items=2, max_items=2) = Field(..., description='(x,y) scaling percent')


class OpacityTransformOperation(TransformOperation):
    type: Literal[OperationType.Opacity] = OperationType.Opacity
    value: conint(ge=0, le=100) = Field(..., description='opacity percent')


class SkewTransformOperation(TransformOperation):
    type: Literal[OperationType.Skew] = OperationType.Skew
    value: confloat(ge=0, lt=360) = Field(..., description='skew amount degrees')
    axis: Optional[confloat(ge=0, lt=360)] = Field(default=0, description='skew axis (0 skews along the X axis, 90 along the Y axis)')


# merges
class MergeOperation(OperationBase):
    type: Literal[OperationType.Merge] = OperationType.Merge
    animations: list[Lottie] = Field(..., description='list of lotties to merge')


# all operations
LottieOperation = Union[
    RotationTransformOperation,
    PositionTransformOperation,
    ScalingTransformOperation,
    MergeOperation
]

if __name__ == '__main__':
    import json
    from pydantic import parse_raw_as

    # encode
    operations = [
        {'type': OperationType.Rotation, 'element_id': '111', 'value': 15.0},
        {'type': OperationType.Position, 'element_id': '222', 'value': [10, 20]},
        {'type': OperationType.Scaling, 'element_id': '333', 'value': [50, 50]},
        {'type': OperationType.Merge, 'animations': [{'a': 1}, {'b': 2}]}
    ]
    encoded = json.dumps(operations)

    # decode
    parsed = parse_raw_as(list[LottieOperation], encoded)

    # assert
    expected = [
        RotationTransformOperation(element_id='111', value=15.0),
        PositionTransformOperation(element_id='222', value=[10, 20]),
        ScalingTransformOperation(element_id='333', value=[50, 50]),
        MergeOperation(animations=[{'a': 1}, {'b': 2}])
    ]
    assert not any(a != b for a, b in zip(parsed, expected)), '*** Parse failed! ***'
