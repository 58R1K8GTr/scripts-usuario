"""Tests for types_project module."""
import pytest
from src.types_project import NumberPosition


def test_number_position_valid():
    """Test NumberPosition with valid inputs."""
    pos = NumberPosition(vertical=1, horizontal=2)
    assert pos.vertical == 1
    assert pos.horizontal == 2


@pytest.mark.parametrize("v, h", [
    (0, 1), (4, 1), (1, 0), (1, 4)
])
def test_number_position_invalid_vertical(v, h):
    """Test NumberPosition with invalid vertical or horizontal inputs."""
    with pytest.raises(ValueError):
        NumberPosition(vertical=v, horizontal=h)


def test_number_position_iter():
    """Test iteration over NumberPosition."""
    pos = NumberPosition(vertical=3, horizontal=1)
    h, v = pos
    assert h == 1
    assert v == 3
