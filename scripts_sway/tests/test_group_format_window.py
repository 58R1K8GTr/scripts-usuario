"""Tests for GroupFormatWindowState and HorizontalLineState."""

from unittest.mock import MagicMock

import pytest

from src.group_format_window import HorizontalLineState, VerticalLineState
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
def vertical_line_state(default_screen_size, default_mark_sizes, initial_positions):
    """Fixture for VerticalLineState instance."""
    return VerticalLineState(default_screen_size, default_mark_sizes, initial_positions)


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

    # Test move_down (increases value towards 3)
    # V: 1 -> 2
    horizontal_line_state.move_down()
    assert horizontal_line_state._positions.vertical == 2
    # V: 2 -> 3
    horizontal_line_state.move_down()
    assert horizontal_line_state._positions.vertical == 3
    # V: 3 -> 3 (max)
    horizontal_line_state.move_down()
    assert horizontal_line_state._positions.vertical == 3

    # Test move_up (decreases value towards 1)
    # V: 3 -> 2
    horizontal_line_state.move_up()
    assert horizontal_line_state._positions.vertical == 2
    # V: 2 -> 1
    horizontal_line_state.move_up()
    assert horizontal_line_state._positions.vertical == 1
    # V: 1 -> 1 (min)
    horizontal_line_state.move_up()
    assert horizontal_line_state._positions.vertical == 1


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


def test_horizontal_line_left_organize_move(horizontal_line_state):
    """Test organizing all windows on 1, 1."""
    windows = [MagicMock(spec=Window) for _ in range(26)]
    horizontal_line_state.organize(windows, 'popup')
    positions = (0, 5, 25)
    coordenates = ((1536, 864), (1536, 648), (1536, 864))
    for position, coordenate in zip(positions, coordenates):
        x, y = coordenate
        command = f"absolute position {x} {y}"
        windows[position].move.assert_called_once_with(command)


def test_horizontal_line_right_organize_move(horizontal_line_state):
    """Test organizing all windows on 3, 1."""
    windows = [MagicMock(spec=Window) for _ in range(26)]
    horizontal_line_state.move_left()
    horizontal_line_state.move_left()
    assert horizontal_line_state._positions == NumberPosition(3, 1)
    horizontal_line_state.organize(windows, 'popup')
    positions = (0, 5, 25)
    coordenates = ((0, 864), (0, 648), (0, 864))
    for position, coordenate in zip(positions, coordenates):
        x, y = coordenate
        command = f"absolute position {x} {y}"
        windows[position].move.assert_called_once_with(command)


def test_horizontal_line_center_organize_move(horizontal_line_state):
    """Test organizing all windows on 2, 1."""
    windows = []
    for _ in range(26):
        window = MagicMock(spec=Window)
        window.mark = ''
        windows.append(window)
    horizontal_line_state.move_left()
    assert horizontal_line_state._positions == NumberPosition(2, 1)
    horizontal_line_state.organize(windows, 'popup')
    positions = (0, 1, 2, 4, 5, 24, 25)
    coordenates = ((768, 864), (1152, 864), (384, 864), (0, 864),
                   (768, 648), (0, 0), (768, 864))
    for position, coordenate in zip(positions, coordenates):
        x, y = coordenate
        command = f"absolute position {x} {y}"
        windows[position].move.assert_called_with(command)


def test_vertical_line_top_organize_move(vertical_line_state):
    """Test organizing all windows on 1, 1."""
    windows = [MagicMock(spec=Window) for _ in range(26)]
    vertical_line_state.organize(windows, 'popup')
    positions = (0, 1, 4, 5, 25)
    coordenates = ((0, 0), (0, 216), (0, 864), (384, 0), (0, 0))
    for position, coordenate in zip(positions, coordenates):
        x, y = coordenate
        command = f"absolute position {x} {y}"
        windows[position].move.assert_called_once_with(command)


def test_vertical_line_bottom_organize_move(vertical_line_state):
    """Test organizing all windows on 1, 1."""
    windows = [MagicMock(spec=Window) for _ in range(26)]
    vertical_line_state.move_down()
    vertical_line_state.move_down()

    assert vertical_line_state._positions == NumberPosition(1, 3)

    vertical_line_state.organize(windows, 'popup')

    positions = (0, 1, 4, 5, 25)
    coordenates = ((0, 864), (0, 648), (0, 0), (384, 864), (0, 864))
    for position, coordenate in zip(positions, coordenates):
        x, y = coordenate
        command = f"absolute position {x} {y}"
        windows[position].move.assert_called_once_with(command)
