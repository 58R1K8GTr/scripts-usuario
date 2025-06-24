"""Tests for Window implementations."""
from unittest.mock import Mock, MagicMock, patch

import pytest
from rich.console import Console

from src.windows import WindowCon, NoWindowCon


@pytest.fixture
def mock_i3_con():
    """Fixture for a mocked i3ipc.Con object."""
    con = MagicMock()
    con.name = "Test Window"
    con.marks = []
    con.focused = False
    con.rect = Mock()
    return con


@pytest.fixture
def window_con(mock_i3_con):
    """Fixture for WindowCon instance."""
    return WindowCon(mock_i3_con)


def test_window_con_name(window_con, mock_i3_con):
    assert window_con.name == "Test Window"


def test_window_con_set_mark(window_con, mock_i3_con):
    window_con.set_mark("test_mark").execute()
    mock_i3_con.command.assert_called_once_with("mark test_mark")


def test_window_con_enable_float(window_con, mock_i3_con):
    window_con.enable_float().execute()
    # Called multiple times due to sleep
    mock_i3_con.command.assert_called_with("floating enable")


def test_window_con_marks_empty(window_con, mock_i3_con):
    mock_i3_con.marks = []
    assert window_con.marks() == []
    assert window_con.mark == ""


def test_window_con_marks_present(window_con, mock_i3_con):
    mock_i3_con.marks = ["popup_1", "another_mark"]
    assert window_con.marks() == ["popup_1", "another_mark"]
    assert window_con.mark == "popup_1"


def test_window_con_float_type(window_con, mock_i3_con):
    mock_i3_con.marks = ["popup_special_1"]
    assert window_con.float_type == "popup"
    mock_i3_con.marks = []
    assert window_con.float_type == ""


# Tests for NoWindowCon
@pytest.fixture
def no_window_con():
    return NoWindowCon()


@patch('src.windows.rich_print')
def test_no_window_con_name(mock_rich_print, no_window_con):
    assert no_window_con.name == ""
    mock_rich_print.assert_called_once_with(
        'log name: [red]No window selected.[/]')


@patch('src.windows.rich_print')
def test_no_window_con_set_mark(mock_rich_print, no_window_con):
    no_window_con.set_mark("test_mark")
    mock_rich_print.assert_called_once_with(
        'log set_mark: [red]No window selected.[/]')


@patch('src.windows.rich_print')
def test_no_window_con_marks(mock_rich_print, no_window_con):
    assert no_window_con.marks() == []
    mock_rich_print.assert_called_once_with(
        'log marks: [red]No window selected.[/]')


@patch('src.windows.rich_print')
def test_no_window_con_mark_property(mock_rich_print, no_window_con):
    assert no_window_con.mark == ""
    mock_rich_print.assert_called_once_with(
        'log mark: [red]No window selected.[/]')
