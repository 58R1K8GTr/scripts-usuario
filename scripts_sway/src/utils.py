"""Functions without a especific module."""

from typing import Any


def slice_group(items: list[Any],  group_size: int) -> list[list[Any]]:
    """Slice a list in a  list of lists."""
    return [items[i:i + group_size] for i in range(0, len(items), group_size)]
