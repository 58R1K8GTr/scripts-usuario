"""Tests for SwayManager."""
from unittest.mock import Mock, patch, MagicMock

import pytest

from src.sway_manager import SwayManager
from src.windows import WindowCon, NoWindowCon
from src.types_project import NumberPosition


@pytest.fixture
def mock_i3_connection():
    """Fixture for a mocked i3ipc Connection."""
    conn = Mock()
    output_mock = Mock()
    output_mock.active = True
    output_mock.rect.width = 1920
    output_mock.rect.height = 1080
    conn.get_outputs.return_value = [output_mock]
    conn.get_tree.return_value = MagicMock()
    conn.get_marks.return_value = []
    return conn


@pytest.fixture
def sway_manager(mock_i3_connection):
    """Fixture for SwayManager instance."""
    rect = (1920, 1080)
    mark_sizes = {
        'popup': list(map(lambda x: x // 100 * 20, rect)),
        'medium': list(map(lambda x: x // 100 * 40, rect)),
        'large': list(map(lambda x: x // 100 * 60, rect))
    }
    return SwayManager(mock_i3_connection, rect, mark_sizes)


def test_sway_manager_initialization(sway_manager, mock_i3_connection):
    """Test SwayManager initialization."""
    assert sway_manager._SwayManager__con == mock_i3_connection
    assert 'popup' in sway_manager._SwayManager__mark_sizes
    assert isinstance(
        sway_manager._SwayManager__state._positions, NumberPosition)


def test_get_windows_by_mark_no_windows(sway_manager, mock_i3_connection):
    """Test get_windows_by_mark when no windows match."""
    mock_i3_connection.get_tree.return_value.find_marked.return_value = []
    assert sway_manager.get_windows_by_mark('popup') == []


def test_get_windows_by_mark_with_windows(sway_manager, mock_i3_connection):
    """Test get_windows_by_mark when windows match."""
    mock_con1 = Mock(spec=WindowCon)
    mock_con1.pid = 123
    mock_con1.name = "Window1"
    mock_con2 = Mock(spec=WindowCon)
    mock_con2.pid = 456
    mock_con2.name = "Window2"

    mock_i3_connection.get_tree.return_value.find_marked.return_value = [
        mock_con1, mock_con2]

    with patch('src.sway_manager.WindowCon', side_effect=lambda x: x) as mock_window_con_init:
        windows = sway_manager.get_windows_by_mark('popup')
        assert len(windows) == 2
        assert windows[0] == mock_con1
        assert windows[1] == mock_con2
        mock_window_con_init.assert_any_call(mock_con1)
        mock_window_con_init.assert_any_call(mock_con2)


def test_get_focused_window_none_focused(sway_manager, mock_i3_connection):
    """Test __get_focused_window when no window is focused."""
    mock_i3_connection.get_tree.return_value.find_focused.return_value = None
    assert isinstance(
        sway_manager._SwayManager__get_focused_window, NoWindowCon)


def test_get_focused_window_is_focused(sway_manager, mock_i3_connection):
    """Test __get_focused_window when a window is focused."""
    focused_mock = Mock()
    focused_mock.pid = 123
    mock_i3_connection.get_tree.return_value.find_focused.return_value = focused_mock
    with patch('src.sway_manager.WindowCon') as mock_window_con_init:
        sway_manager._SwayManager__get_focused_window
        mock_window_con_init.assert_called_once_with(focused_mock)


def test_generate_new_mark_name_no_existing(sway_manager, mock_i3_connection):
    """Test __generate_new_mark_name with no existing marks of that type."""
    mock_i3_connection.get_marks.return_value = []
    assert sway_manager._SwayManager__generate_new_mark_name(
        'popup') == 'popup_1'


def test_generate_new_mark_name_with_existing(sway_manager, mock_i3_connection):
    """Test __generate_new_mark_name with existing marks."""
    mock_i3_connection.get_marks.return_value = [
        'popup_1', 'other_1', 'popup_2']
    assert sway_manager._SwayManager__generate_new_mark_name(
        'popup') == 'popup_3'
    mock_i3_connection.get_marks.return_value = ['popup_10', 'popup_1']
    assert sway_manager._SwayManager__generate_new_mark_name(
        'popup') == 'popup_11'


@patch('src.sway_manager.SwayManager._SwayManager__get_focused_window', new_callable=MagicMock)
def test_transform_focused_as_popup(mock_get_focused, sway_manager):
    """Test transform_focused_as popup."""
    mock_window = MagicMock(spec=WindowCon)
    mock_window.mark = ''  # No existing mark
    mock_get_focused.return_value = mock_window

    sway_manager.transform_as_popup()

    mock_window.set_mark.assert_called_once_with('popup_1')
    mock_window.enable_float.assert_called_once()
    mock_window.resize.assert_called_once()
    mock_window.enable_sticky.assert_called_once()


@patch('src.sway_manager.SwayManager._SwayManager__get_focused_window', new_callable=MagicMock)
def test_transform_focused_as_already_marked(mock_get_focused, sway_manager):
    """Test transform_focused_as when window is already marked."""
    mock_window = MagicMock(spec=WindowCon)
    mock_window.mark = 'existing_mark_1'  # Window already has a mark
    mock_get_focused.return_value = mock_window

    result_window = sway_manager.transform_focused_as('popup')
    assert isinstance(result_window, NoWindowCon)
    mock_window.set_mark.assert_not_called()


def test_move_methods_call_state_and_organize(sway_manager):
    """Test that move methods call state methods and organize."""
    mock_state = MagicMock()
    sway_manager._SwayManager__state = mock_state
    sway_manager.get_windows_by_mark = MagicMock(
        return_value=[])  # Mock to avoid i3ipc calls

    sway_manager.move_left('popup')
    mock_state.move_left.assert_called_once()
    mock_state.organize.assert_called_with([], 'popup')
    mock_state.reset_mock()

    sway_manager.move_right('popup')
    mock_state.move_right.assert_called_once()
    mock_state.organize.assert_called_with([], 'popup')
    mock_state.reset_mock()

    sway_manager.move_up('popup')
    mock_state.move_up.assert_called_once()
    mock_state.organize.assert_called_with([], 'popup')
    mock_state.reset_mock()

    sway_manager.move_down('popup')
    mock_state.move_down.assert_called_once()
    mock_state.organize.assert_called_with([], 'popup')
