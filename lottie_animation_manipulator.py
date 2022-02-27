from vidalgo_lottie_base import Vidalgo_lottie_base
from dataclasses import dataclass


# TODO: move dataclasses to a separate file
@dataclass
class OperationBase:
    element_id: str


@dataclass
class RotationOperation(OperationBase):
    deg: float


@dataclass
class RecolorOperation(OperationBase):
    colors: list[int]  # TODO: define Color type


@dataclass
class CombineOperation(OperationBase):
    other: Vidalgo_lottie_base
    position: list[int] # TODO: type PosVector or 2Vec


class LottieAnimationManipulator:
    def __init__(self, lottie: Vidalgo_lottie_base):
        self._lottie = lottie

    def apply_changes(self, changes: list[OperationBase]) -> None:
        for change in changes:
            self._apply_single_change(change)

    @property
    def lottie(self):
        return self._lottie

    def _apply_single_change(self, operation: OperationBase):
        if isinstance(operation, RotationOperation):
            self._rotate(operation)
        elif isinstance(operation, RecolorOperation):
            self._change_color(operation)
        else:
            raise ValueError('unsupported change type')


if __name__ == '__main__':
    lottie = None # load_lottie(file) # TODO: lottie = load_lottie(file)
    lm = LottieAnimationManipulator(lottie=lottie)
    lm.apply_changes(RotationOperation(element_id='e1', deg=70))
    print(lm.lottie)
