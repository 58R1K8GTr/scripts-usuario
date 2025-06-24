"""Interface cli."""


from click import command
from i3ipc import Connection
from i3ipc.events import Event
from rich import print as rich_print

from src.binding import SwayBindingHandler
from src.sway_manager import SwayManager


def main():
    """The asynchronous main function."""
    ipc = Connection(auto_reconnect=True)
    manager = SwayManager.create(ipc)
    handler = SwayBindingHandler(manager)

    def on_binding(connection, event):
        handler.handle_binding_event(connection, event)

    ipc.on(Event.BINDING, on_binding)
    ipc.main()


@command
# @option('--debug')?
def cli() -> None:
    """sway auxiliary script commands."""
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        rich_print("[blue]\nExiting.[/]")
    except Exception as error:
        rich_print(f"[red]{error}")
