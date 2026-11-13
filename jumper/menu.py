from collections.abc import Callable
from dataclasses import dataclass


@dataclass
class JumpParameter:
    name: str
    get_value: Callable[[], int]
    set_value: Callable[[int], None]
    min: int = 1
    max: int = 100
    step: int = 1
    unit: str = ""

    def _adjust(self, direction: int) -> None:
        clamp = lambda v, v0, v1: max(v0, min(v, v1))

        new_value = self.get_value() + direction * self.step
        new_value = clamp(new_value, self.min, self.max)

        self.set_value(new_value)

    def up(self) -> None:
        self._adjust(1)

    def down(self) -> None:
        self._adjust(-1)

    def format(self) -> str:
        return f"{self.name}: {self.get_value()}{self.unit}"


class JumpMenu:
    def __init__(self, params: list[JumpParameter]):
        if not params:
            raise ValueError("JumpParameter list cannot be empty")

        self.params = params
        self._selected_index = 0

    @property
    def selected(self) -> JumpParameter:
        return self.params[self._selected_index]

    def _advance(self, n: int) -> None:
        self._selected_index = (self._selected_index + n) % len(self.params)

    def next(self) -> None:
        self._advance(1)

    def prev(self) -> None:
        self._advance(-1)
