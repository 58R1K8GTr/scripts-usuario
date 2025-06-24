"""Types."""


from typing import TypedDict, Literal, Iterator
from dataclasses import dataclass


class StatusValidation(TypedDict):
    """Status and message for a validation."""
    status: bool
    message: str | None


PositionHeadListType = Literal['right', 'center', 'left']
MarkType = Literal['popup', 'medium', 'large']


NumberPositionType = Literal[1, 2, 3]

# TuplePositionType = tuple[NumberPositionType, NumberPositionType]

MarkSizeType = dict[MarkType, list[int]]


@dataclass
class NumberPosition:
    """Position of groups"""
    vertical: NumberPositionType
    horizontal: NumberPositionType

    def __post_init__(self):
        range_int = range(1, 4)
        if self.vertical not in range_int:
            raise ValueError("Acepted vertical values: 1, 2 or 3.")
        if self.horizontal not in range_int:
            raise ValueError("Acepted horizontal values: 1, 2 or 3.")

    def __iter__(self) -> Iterator:
        return iter((self.horizontal, self.vertical))
