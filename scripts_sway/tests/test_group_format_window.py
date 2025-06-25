"""Tests for GroupFormatWindowState and HorizontalLineState."""

from unittest.mock import MagicMock

import pytest

from src.group_format_window import HorizontalLineState
from src.types_project import NumberPosition, MarkSizeType
from src.windows import Window


@pytest.fixture
def default_screen_size():
    return (1920, 1080)


@pytest.fixture
def default_mark_sizes() -> MarkSizeType:
    return {'popup': [384, 216]}  # 20%


@pytest.fixture
def initial_positions():
    return NumberPosition(1, 1)


@pytest.fixture
def horizontal_line_state(default_screen_size, default_mark_sizes, initial_positions):
    """Fixture for HorizontalLineState instance."""
    return HorizontalLineState(default_screen_size, default_mark_sizes, initial_positions)


@pytest.fixture
def windows_data(default_mark_sizes, default_screen_size):
    """Fixture to return windows data."""
    windows_number = 26
    windows = [MagicMock(spec=Window) for _ in range(windows_number)]
    mark_name = 'popup'

    mark_width, mark_height = default_mark_sizes[mark_name]
    screen_width, screen_height = default_screen_size
    max_x_windows = screen_width // mark_width
    max_y_windows = screen_height // mark_height

    def calculate(number_window) -> tuple[int, int]:
        # Expected for window1 (n=0)
        expected_x1 = (
            screen_width - mark_width * (number_window % max_x_windows + 1)
        )
        expected_y1 = (
            screen_height - mark_height *
            (number_window // max_x_windows % max_y_windows + 1)
        )
        return (expected_x1, expected_y1)

    indexes = [calculate(n) for n in range(windows_number)]
    return (windows, indexes)


def test_group_format_window_state_movements(horizontal_line_state):
    """Test movement methods of GroupFormatWindowState."""
    # Initial state: horizontal=1, vertical=1

    # Test move_left
    horizontal_line_state.move_left()  # H: 1 -> 2
    assert horizontal_line_state._positions.horizontal == 2
    horizontal_line_state.move_left()  # H: 2 -> 3
    assert horizontal_line_state._positions.horizontal == 3
    horizontal_line_state.move_left()  # H: 3 -> 3 (max)
    assert horizontal_line_state._positions.horizontal == 3

    # Test move_right
    horizontal_line_state.move_right()  # H: 3 -> 2
    assert horizontal_line_state._positions.horizontal == 2
    horizontal_line_state.move_right()  # H: 2 -> 1
    assert horizontal_line_state._positions.horizontal == 1
    horizontal_line_state.move_right()  # H: 1 -> 1 (min)
    assert horizontal_line_state._positions.horizontal == 1

    # Test move_up (current logic: value = max(1, self._positions.vertical + 1))
    # V: 1 -> 2
    horizontal_line_state.move_up()
    assert horizontal_line_state._positions.vertical == 2
    # V: 2 -> 3
    horizontal_line_state.move_up()
    assert horizontal_line_state._positions.vertical == 3
    # V: 3 -> 4 (Note: this exceeds NumberPositionType Literal[1,2,3])
    # The cast(NumberPositionType, value) might be an issue at runtime elsewhere
    # or with stricter type checking, but we test the method's direct output.
    horizontal_line_state.move_up()
    assert horizontal_line_state._positions.vertical == 4

    # Reset vertical position for move_down test
    horizontal_line_state._positions.vertical = 3

    # Test move_down (current logic: value = min(3, self._positions.vertical - 1))
    # V: 3 -> 2
    horizontal_line_state.move_down()
    assert horizontal_line_state._positions.vertical == 2
    # V: 2 -> 1
    horizontal_line_state.move_down()
    assert horizontal_line_state._positions.vertical == 1
    # V: 1 -> 0 (Note: this is below NumberPositionType Literal[1,2,3])
    horizontal_line_state.move_down()
    assert horizontal_line_state._positions.vertical == 0


def test_horizontal_line_state_organize_no_windows(horizontal_line_state):
    """Test organize with no windows."""
    horizontal_line_state.organize([], 'popup')
    # No error should occur, and nothing should happen


def test_horizontal_line_state_organize_one_window(horizontal_line_state, default_screen_size, default_mark_sizes):
    """Test organize with one window."""
    mock_window = MagicMock(spec=Window)
    windows = [mock_window]
    mark_name = 'popup'
    mark_width, mark_height = default_mark_sizes[mark_name]
    screen_width, screen_height = default_screen_size

    # Expected position for the first window (n=0)
    # max_x_windows = screen_width // mark_width
    # x = screen_width - mark_width * (0 % max_x_windows + 1)
    # y = screen_height - mark_height * (0 // max_x_windows + 1)
    expected_x = screen_width - mark_width
    expected_y = screen_height - mark_height

    horizontal_line_state.organize(windows, mark_name)
    mock_window.move.assert_called_once_with(
        f"absolute position {expected_x} {expected_y}")


def test_horizontal_line_state_organize_multiple_windows(horizontal_line_state, default_screen_size, default_mark_sizes):
    """Test organize with multiple windows."""
    mock_window1 = MagicMock(spec=Window)
    mock_window2 = MagicMock(spec=Window)
    windows = [mock_window1, mock_window2]
    mark_name = 'popup'

    mark_width, mark_height = default_mark_sizes[mark_name]
    screen_width, screen_height = default_screen_size
    max_x_windows = screen_width // mark_width

    # Expected for window1 (n=0)
    expected_x1 = screen_width - mark_width * (0 % max_x_windows + 1)
    expected_y1 = screen_height - mark_height * (0 // max_x_windows + 1)

    # Expected for window2 (n=1)
    expected_x2 = screen_width - mark_width * (1 % max_x_windows + 1)
    expected_y2 = screen_height - mark_height * (1 // max_x_windows + 1)

    horizontal_line_state.organize(windows, mark_name)

    mock_window1.move.assert_called_once_with(
        f"absolute position {expected_x1} {expected_y1}")
    mock_window2.move.assert_called_once_with(
        f"absolute position {expected_x2} {expected_y2}")


def test_horizontal_line_state_organize_position_not_one(horizontal_line_state):
    """Test organize when horizontal position is not 1."""
    mock_window = MagicMock(spec=Window)
    windows = [mock_window]
    mark_name = 'popup'

    # Set horizontal position to something other than 1
    horizontal_line_state._positions.horizontal = 2
    horizontal_line_state.organize(windows, mark_name)
    mock_window.move.assert_not_called()

    horizontal_line_state._positions.horizontal = 3
    horizontal_line_state.organize(windows, mark_name)
    mock_window.move.assert_not_called()


def test_horizontal_line_left_organize_move(horizontal_line_state, windows_data):
    """Test organizing all windows on 1, 1."""
    windows, indexes = windows_data
    horizontal_line_state.organize(windows, 'popup')
    for number in range(26):
        x, y = indexes[number]
        command = f"absolute position {x} {y}"
        windows[number].move.assert_called_once_with(command)
