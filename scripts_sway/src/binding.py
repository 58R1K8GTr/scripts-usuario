"""Creating binds and connection."""

from typing import Any

from i3ipc import Connection
from i3ipc.events import IpcBaseEvent
from rich import print as rich_print


class SwayBindingHandler:
    """Handles sway binding events and dispatches actions."""

    def __init__(self, app_controller: Any):
        self.__app_controller = app_controller
        self.__bindings_map = {
            'Mod1+a+Left': self.move_popup_left,
            'Mod1+a+Right': self.move_popup_right,
            'Mod1+a+Up': self.move_popup_up,
            'Mod1+a+Down': self.move_popup_down,
            'Mod1+p': self.transform_and_organize_popup,
            'Mod1+o': self.organize_popup,
            'Mod1+Shift+Delete': self.quit_application,
        }

    def handle_binding_event(
        self, connection: Connection, event: IpcBaseEvent
    ) -> None:
        """Receives a binding event and calls the appropriate handler."""
        bind_tuple = '+'.join(
            event.binding.event_state_mask +  # type: ignore
            event.binding.symbols  # type: ignore
        )
        handler_method = self.__bindings_map.get(bind_tuple)
        if handler_method:
            handler_method(connection)
        # print(bind_tuple)

    def move_popup_left(self, *_) -> None:
        """Move windows to left."""
        self.__app_controller.move_left('popup')

    def move_popup_right(self, *_) -> None:
        """Move windows to right."""
        self.__app_controller.move_right('popup')

    def move_popup_up(self, *_) -> None:
        """Move windows to up."""
        self.__app_controller.move_up('popup')

    def move_popup_down(self, *_) -> None:
        """Move windows to down."""
        self.__app_controller.move_down('popup')

    def transform_and_organize_popup(self, *_) -> None:
        """Transform and organize popup."""
        self.__app_controller.transform_as_popup()
        self.organize_popup()

    def organize_popup(self, *_) -> None:
        """Organize windows."""
        self.__app_controller.organize_popup()

    def quit_application(self, con: Connection) -> None:
        """Quit application."""
        rich_print('[blue]Bye bye![/]')
        con.main_quit()
