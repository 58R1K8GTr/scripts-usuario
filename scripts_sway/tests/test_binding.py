"""Tests for SwayBindingHandler."""
from unittest.mock import Mock, MagicMock

import pytest

from src.binding import SwayBindingHandler


@pytest.fixture
def mock_app_controller():
    """Fixture for a mocked application controller (SwayManager)."""
    return MagicMock()


@pytest.fixture
def binding_handler(mock_app_controller):
    """Fixture for SwayBindingHandler instance."""
    return SwayBindingHandler(mock_app_controller)


def create_mock_binding_event(mask, symbols):
    """Helper to create a mock binding event."""
    event = Mock()
    event.binding.event_state_mask = mask
    event.binding.symbols = symbols
    return event


def test_handle_binding_event_move_popup_left(binding_handler, mock_app_controller):
    """Test handling of 'Mod1+a+Left' binding."""
    mock_connection = Mock()
    event = create_mock_binding_event(['Mod1', 'a'], ['Left'])
    binding_handler.handle_binding_event(mock_connection, event)
    mock_app_controller.move_left.assert_called_once_with('popup')


def test_handle_binding_event_transform_as_popup(binding_handler, mock_app_controller):
    """Test handling of 'Mod1+p' binding."""
    mock_connection = Mock()
    event = create_mock_binding_event(['Mod1'], ['p'])
    binding_handler.handle_binding_event(mock_connection, event)
    mock_app_controller.transform_as_popup.assert_called_once()


def test_handle_binding_event_quit_application(binding_handler, mock_app_controller):
    """Test handling of 'Mod1+Shift+Delete' binding."""
    mock_connection = MagicMock()  # Needs main_quit
    event = create_mock_binding_event(['Mod1', 'Shift'], ['Delete'])
    binding_handler.handle_binding_event(mock_connection, event)
    mock_connection.main_quit.assert_called_once()


def test_handle_binding_event_unknown_binding(binding_handler, mock_app_controller):
    """Test handling of an unknown binding."""
    mock_connection = Mock()
    event = create_mock_binding_event(['Control'], ['Unknown'])
    binding_handler.handle_binding_event(mock_connection, event)
    # No method on app_controller should be called for unknown bindings
    # (except for the default lambda, which does nothing)
    mock_app_controller.assert_not_called()  # Check if any method was called
    # More specific: check that specific known methods were not called
    mock_app_controller.move_left.assert_not_called()
    mock_app_controller.transform_as_popup.assert_not_called()


def test_move_popup_down_typo_call(binding_handler, mock_app_controller):
    """Test that move_popup_down calls the correct method (handling potential typo)."""
    # This test is specifically for the 'move_dowm' typo in the original binding.py
    binding_handler.move_popup_down(Mock())
    mock_app_controller.move_down.assert_called_once_with(
        'popup')  # Assuming typo is fixed in SwayManager
