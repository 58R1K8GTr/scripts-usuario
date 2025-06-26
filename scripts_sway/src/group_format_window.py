"""A list with a head node."""


from abc import ABC, abstractmethod
from typing import cast

from i3ipc.model import Rect

from src.types_project import (
    NumberPosition, NumberPositionType, MarkType, MarkSizeType
)
from src.windows import WindowCon
# from src.utils import slice_group


class GroupFormatWindowState(ABC):
    """A representation of a group format window."""

    # passar o marksizetype para tupla[int int]?
    def __init__(
        self, screen_size: tuple[int, int],
        mark_sizes: MarkSizeType, positions: NumberPosition
    ) -> None:
        self._screen_size = screen_size
        self._mark_sizes = mark_sizes
        self._positions = positions

    @abstractmethod
    def organize(
        self, windows: dict[str, Rect],
        mark_name: MarkType
    ) -> dict[str, str]:
        """Calculate and position windows."""

    def move_left(self) -> None:
        """Move items to left."""
        value = min(3, self._positions.horizontal + 1)
        self._positions.horizontal = cast(NumberPositionType, value)

    def move_right(self) -> None:
        """Move items to right."""
        value = max(1, self._positions.horizontal - 1)
        self._positions.horizontal = cast(NumberPositionType, value)

    def move_up(self) -> None:
        """Move items to up."""
        value = max(1, self._positions.vertical + 1)
        self._positions.vertical = cast(NumberPositionType, value)

    def move_down(self) -> None:
        """Move items to dowm."""
        value = min(3, self._positions.vertical - 1)
        self._positions.vertical = cast(NumberPositionType, value)


class HorizontalLineState(GroupFormatWindowState):
    """A representation of a group in horizontal line format."""

    # def __center_organize(
    #     self, windows: list[WindowCon], mark_size: list[int]
    # ) -> None:
    #     """Organize windows to center."""
    #     window_width = mark_size[0]
    #     window_height = mark_size[1]
    #     max_x_windows = self._screen_size[0] // window_width
    #     windows[0].move(f"absolute position {x} {y}").execute()
    #     for n, window in enumerate(windows[1:]):
    #         x = self._screen_size[0] - window_width * (n % max_x_windows + 1)
    #         y = self._screen_size[1] - window_height * (n // max_x_windows + 1)
    #         window.move(f"absolute position {x} {y}").execute()
    #         print(x, y, window.mark)

    def __left_organize(
        self, windows: list[WindowCon], mark_size: list[int]
    ) -> None:
        """Organize windows from right to left."""
        window_width = mark_size[0]
        window_height = mark_size[1]
        max_x_windows = self._screen_size[0] // window_width
        max_y_windows = self._screen_size[1] // window_height
        for n, window in enumerate(windows):
            x_up = n % max_x_windows + 1
            y_up = n // max_x_windows % max_y_windows + 1
            x = self._screen_size[0] - window_width * x_up
            y = self._screen_size[1] - window_height * y_up
            window.move(f"absolute position {x} {y}").execute()
            print(x, y, window.mark)

    def __right_organize(
        self, windows: list[WindowCon], mark_size: list[int]
    ) -> None:
        """Organize windows from right to left."""
        window_width = mark_size[0]
        window_height = mark_size[1]
        max_x_windows = self._screen_size[0] // window_width
        max_y_windows = self._screen_size[1] // window_height
        for n, window in enumerate(windows):
            x_up = n % max_x_windows
            y_up = n // max_x_windows % max_y_windows + 1
            x = window_width * x_up % self._screen_size[0]
            y = self._screen_size[1] - window_height * y_up
            window.move(f"absolute position {x} {y}").execute()
            print(x, y, window.mark)

    def organize(
        self, windows: list[WindowCon], mark_name: MarkType
    ) -> None:
        # horizontal, vertical
        if len(windows) == 0:
            return
        positions = self._positions
        mark_size = self._mark_sizes[mark_name]
        if positions.horizontal == 1:
            self.__left_organize(windows, mark_size)
        if positions.horizontal == 3:
            self.__right_organize(windows, mark_size)
        print(positions)


# square, plus?, 4corners?
